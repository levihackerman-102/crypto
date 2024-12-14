#![allow(unused, unreachable_code)]
use ark_ed_on_bls12_381::{EdwardsAffine as GAffine, EdwardsProjective as GProjective, Fr};
use ark_ff::Field;
use ark_std::rand;
use ark_std::{
    io::{Read, Write},
    UniformRand,
};
use rand::{Rng, SeedableRng};
use rand_chacha::ChaChaRng;
use strong_adaptivity::{Instance, Proof, data::puzzle_data, ProofCommitment, ProofResponse};
use strong_adaptivity::{msg_equality_arg, verify};
use strong_adaptivity::PUZZLE_DESCRIPTION;
use prompt::{puzzle, welcome};

fn main() {
    welcome();
    puzzle(PUZZLE_DESCRIPTION);
    let ck = puzzle_data();

    let (instance, witness, proof): (Instance, (Fr, Fr, Fr, Fr), Proof) = {
        let rng = &mut rand::thread_rng();

        // === CHANGE: DEFER OFFLINE PHASE ===
    
        // === ONLINE PHASE ===
        // Step 1: Prover samples random elements r, ρ, τ.
        // CHEAT: generate 2 random r values instead of 1
        let r_rho = Fr::rand(rng);
        let r_tau = Fr::rand(rng);
        // generate random values rho and tau below using commit_with_rng
    
        // Step 2: Prover computes C_ρ, C_τ
        // create the proof commitment with randomly generated rho and tau
        let (comm_rho, rho) = ck.commit_with_rng(r_rho, rng);
        let (comm_tau, tau) = ck.commit_with_rng(r_tau, rng);
        let commitment = ProofCommitment { comm_rho, comm_tau };
    
        // compute verifier's challenge via Fiat-Shamir: e = H(G, H, comm_rho, comm_tau)
        let challenge = msg_equality_arg::utils::b2s_hash_to_field(&(ck, commitment));
    
        // === BEGIN REORDERED OFFLINE PHASE PART 1: a_1, r_1, r_2, comm_1 ===
        let a_1 = Fr::rand(rng);
    
        // compute comm_1 and generate r_1
        let (comm_1, r_1) = ck.commit_with_rng(a_1, rng);
    
        // generate random r_2
        let r_2 = Fr::rand(rng);
        // === END REORDERED OFFLINE PHASE PART 1 ===
    
        // Step 3: Prover computes s, u, t
        // CHEAT: compute s with r_rho and a_1
        let s = r_rho + challenge * a_1;
    
        // compute u, t honestly
        let u = rho + challenge * r_1;
        let t = tau + challenge * r_2;
        // create the proof response
        let response = ProofResponse { s, u, t };
    
    
        // === BEGIN REORDERED OFFLINE PHASE PART 2: a_2, comm_2 ===
        // CHEAT: compute a_2 from a_1, r_rho, r_tau
        let r_diff = r_tau - r_rho;
        let a_2 = a_1 - r_diff / challenge;
        let comm_2 = ck.commit_with_explicit_randomness(a_2, r_2);
        // === END REORDERED OFFLINE PHASE PART 2 ===
    
    
        // PREPARE STRUCTS FOR SOLUTION VALIDATION
        let instance = Instance { comm_1, comm_2 };
        let witness = (a_1, r_1, a_2, r_2);
        let proof = Proof {
            commitment,
            response,
        };
    
        // return
        (instance, witness, proof)
    };
    
    let (a_1, r_1, a_2, r_2) = witness;

    assert!(verify(&ck, &instance, &proof));
    // Check that commitments are correct
    assert_eq!(ck.commit_with_explicit_randomness(a_1, r_1), instance.comm_1);
    assert_eq!(ck.commit_with_explicit_randomness(a_2, r_2), instance.comm_2);
    // Check that messages are unequal
    assert_ne!(a_1, a_2);
    println!("Proof is valid!");
}