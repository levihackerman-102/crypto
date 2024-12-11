#![allow(unused, unreachable_code)]
use ark_ed_on_bls12_381::Fr;
use ark_ff::Field;
use double_trouble::data::puzzle_data;
use double_trouble::inner_product_argument::utils::challenge;
use double_trouble::verify;
use double_trouble::PUZZLE_DESCRIPTION;
use prompt::{puzzle, welcome};

// Use the publicly known s vectors and the computed verifier challenges from proofs 1 and 2 to
// solve for the random vector r used in proof1 (this was supposed to be a secret nonce!)
// Because comm_r1 * 2 = comm_r2, we know that r = (proof1.response.s - proof2.response.s) / (challenge1 - 2*challenge2)
fn solve_for_r(s1: Vec<Fr>, s2: Vec<Fr>, challenge1: Fr, challenge2: Fr) -> Vec<Fr> {
    // challenge1 - 2 * challenge2
    let challenge_diff = challenge1 - challenge2.double();
    let challenge_diff_inv = challenge_diff.inverse().unwrap();

    let mut r = Vec::with_capacity(s1.capacity());
    for (s1_num, s2_num) in s1.iter().zip(s2.iter()) {
        let s_diff_i = *s1_num - *s2_num;
        let r_i = s_diff_i * challenge_diff_inv;
        r.push(r_i);
    }

    // return r
    r
}

// Use the public s vector and the computed challenge from proof 1 along with our recovered r vector to
// solve for the secret vector a. We could also have done this using known values from proof 2 with double our recovered r
// a = proof1.response.s - challenge1 * r (or a = proof2.response.s - challenge2 * 2 * r)
fn solve_for_a(s1: Vec<Fr>, challenge1: Fr, r: Vec<Fr>) -> Vec<Fr> {
    let mut a = Vec::with_capacity(s1.capacity());

    for (s1_num, r_num) in s1.iter().zip(r.iter()) {
        let a_i = *s1_num - challenge1 * *r_num;
        a.push(a_i);
    }

    // return a
    a
}

// Use the public elements u (computed & shared by prover in each proof) and the computed verifier challenges from proofs 1 and 2 to
// solve for ρ (the randomness used for comm_r in proof 1)
//  ρ = (proof1.response.u - proof2.response.u) / (challenge1 - 2 * challenge2)
fn solve_for_rho(u1: Fr, u2: Fr, challenge1: Fr, challenge2: Fr) -> Fr {
    let challenge_diff_inv = (challenge1 - challenge2.double()).inverse().unwrap();
    // return rho
    (u1 - u2) * challenge_diff_inv
}

// Use the public scalar u and the computed verifier challenge along with our recovered rho value (comm_r_rand) from the first proof to
// solve for alpha, the randomness used in the commitment of our secret vector a
// alpha = proof1.response.u - challenge1 * rho1 (or alpha = u2 - challenge2 * rho2)
fn solve_for_alpha(u1: Fr, challenge1: Fr, rho1: Fr) -> Fr {
    // return alpha
    u1 - challenge1 * rho1
}

fn main() {
    welcome();
    puzzle(PUZZLE_DESCRIPTION);
    let (ck, [instance_and_proof_1, instance_and_proof_2]) = puzzle_data();
    let (instance1, proof1) = instance_and_proof_1;
    let (instance2, proof2) = instance_and_proof_2;
    assert!(verify(&ck, &instance1, &proof1));
    assert!(verify(&ck, &instance2, &proof2));

    let challenge1 = challenge(&ck, &instance1, &proof1.commitment);
    let challenge2 = challenge(&ck, &instance2, &proof2.commitment);

    // STEP 1: USE s1, s2, challenge1, challenge2, TO SOLVE FOR r1
    let r1: Vec<Fr> = solve_for_r(
        proof1.response.s.clone(),
        proof2.response.s.clone(),
        challenge1,
        challenge2,
    );

    // STEP 2: USE s1, challenge1, r1 TO SOLVE FOR a
    let a: Vec<Fr> = solve_for_a(proof1.response.s.clone(), challenge1, r1);

    // STEP 3: USE u1, u2, challenge1, challenge2 TO SOLVE FOR ρ1 (comm_r_rand)
    let comm_r_rand: Fr =
        solve_for_rho(proof1.response.u, proof2.response.u, challenge1, challenge2);

    // STEP 4: USE u, challenge1, comm_r_rand TO SOLVE FOR alpha
    let comm_a_rand: Fr = solve_for_alpha(proof1.response.u, challenge1, comm_r_rand);
    
    assert_eq!(
        ck.commit_with_explicit_randomness(&a, comm_a_rand),
        instance1.comm_a
    );
    assert_eq!(
        ck.commit_with_explicit_randomness(&a, comm_a_rand),
        instance2.comm_a
    );

    println!("Recovered vector a: {:?}", a);
}