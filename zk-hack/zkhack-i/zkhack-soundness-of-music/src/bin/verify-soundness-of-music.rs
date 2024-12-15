#![allow(dead_code)]
#![allow(non_snake_case)]
#![allow(unused_variables)]
#![allow(unreachable_code)]
#![allow(unused_imports)]

use ark_ec::{AffineCurve, PairingEngine, ProjectiveCurve};
use ark_ff::{One, Zero};
use itertools::izip;
use prompt::{puzzle, welcome};
use soundness_of_music::data::puzzle_data;
use soundness_of_music::prover::{prove, Proof};
use soundness_of_music::setup::Setup;
use soundness_of_music::verifier;
use soundness_of_music::PUZZLE_DESCRIPTION;

type Fr = <ark_bls12_381::Bls12_381 as ark_ec::PairingEngine>::Fr;

fn generate_attack_factors<E: PairingEngine>(
    old_public_inputs: &[E::Fr],
    new_public_inputs: &[E::Fr],
    setup: &Setup<E>,
) -> (E::G1Affine, E::G1Affine) {
    let mut pk_eta = E::G1Projective::zero();
    let mut pk_eta_prime = E::G1Projective::zero();
    for (old_input, new_input, public_input_poly, public_input_poly_prime) in izip!(
        old_public_inputs.iter(),
        new_public_inputs.iter(),
        setup.inputs.iter(),
        setup.inputs_prime.iter()
    ) {
        let public_diff = *old_input - *new_input;
        pk_eta += public_input_poly.mul(public_diff);
        pk_eta_prime += public_input_poly_prime.mul(public_diff);
    }
    let pk_eta = pk_eta.into_affine();
    let pk_eta_prime = pk_eta_prime.into_affine();

    (pk_eta, pk_eta_prime)
}

fn main() {
    welcome();
    puzzle(PUZZLE_DESCRIPTION);
    let (circuit, setup) = puzzle_data();

    // the new public inputs for which we want to generate a proof
    let public_inputs = [Fr::one(), Fr::one()];

    // generate the old proof (with the original public/private inputs)
    let two = Fr::one() + Fr::one();
    let four = two + two;
    let old_public_inputs = [Fr::one(), four];
    let private_inputs = [two];
    let old_proof = prove(&old_public_inputs, &private_inputs, &circuit, &setup);

    // PASS VERIFICATION VIA BUG
    // verify the new public inputs using the old proof - this shouldn't work
    // assert!(verifier::verify(&public_inputs, &setup, &old_proof));

    // PASS VERIFICATION VIA ATTACK
    // η_A := π_A + \sum{i=0,n}(x_i - x'_i)*pk_{A,i}
    // η'_A := π'_A + \sum{i=0,n}(x_i - x'_i)*pk'_{A,i}
    let (pk_eta, pk_eta_prime) =
        generate_attack_factors(&old_public_inputs, &public_inputs, &setup);

    // create the attack proofs of pi_input and pi_input_prime
    let eta_a = old_proof.pi_input + pk_eta;
    let eta_a_prime = old_proof.pi_input_prime + pk_eta_prime;

    // π∗ := (ηA, πB, πC, η'A, π'B, π'C, πK, πH)
    let attack_proof = Proof {
        // replace proof of pi_input with scaled input proof
        pi_input: eta_a,
        // replace proof of pi_input_prime with scaled input prime proof
        pi_input_prime: eta_a_prime,
        pi_output: old_proof.pi_output,
        pi_output_prime: old_proof.pi_output_prime,
        pi_K: old_proof.pi_K,
        pi_H: old_proof.pi_H,
    };

    // Verify the attack proof of the new public inputs with the original setup
    assert!(verifier::verify(&public_inputs, &setup, &attack_proof));
    println!("Puzzle solved")
}