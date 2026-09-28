# genpark-reed-solomon-error-correcting-code-skill

Agent Skill implementing **Systematic Reed-Solomon Error-Correcting Code** over Galois Field $GF(2^8)$ with generator polynomial synthesis and syndrome checking.

## Architectural Overview
```mermaid
flowchart TD
    Msg["Raw Data Message M(x)"] --> Gen["Generator Poly g(x) = Prod (x - alpha^i)"]
    Msg & Gen --> Shift["Multiply by x^(2t) & Modular Reduction"]
    Shift --> Parity["Systematic Parity Symbols P(x)"]
    Parity --> Code["Codeword C(x) = [M(x) | P(x)]"]
    Code --> Syn["Syndrome Evaluation S_i = C(alpha^i)"]
    Syn --> Status["Verify Zero Syndromes (Clean Data)"]
```
