from fastapi import APIRouter, Query
from utils.database import get_db
from utils.openai_client import generate_practice_questions
from routes.upload import analysis_store

router = APIRouter()

# Hardcoded question bank per topic (used as seed + fallback)
QUESTION_BANK = {
    "Quantum Mechanics II": [
        {
            "difficulty": "Hard",
            "paper": "Paper 2023, Q4",
            "text": "Evaluate the expectation value of the Hamiltonian for a particle in a one-dimensional box when the wavefunction is a superposition of the first two eigenstates.",
            "answer": "Use ⟨H⟩ = |c₁|²E₁ + |c₂|²E₂. For equal superposition: ⟨H⟩ = (E₁ + E₂)/2 = (π²ℏ²/2mL²)(1 + 4)/2",
            "time": "12 mins"
        },
        {
            "difficulty": "Medium",
            "paper": "Paper 2022, Q1(c)",
            "text": "Derive the time-independent Schrödinger equation starting from the time-dependent form for a stationary state. Explain the physical significance of each term.",
            "answer": "Apply separation of variables Ψ(x,t) = ψ(x)φ(t). The spatial part gives Ĥψ = Eψ where Ĥ = -ℏ²/2m · d²/dx² + V(x).",
            "time": "10 mins"
        },
        {
            "difficulty": "Easy",
            "paper": "Paper 2021, Q9",
            "text": "State the normalization condition for a one-dimensional wavefunction and verify it for a particle in the ground state of an infinite square well.",
            "answer": "∫|ψ|²dx = 1. For infinite square well: ψ₁ = √(2/L)sin(πx/L). Integral from 0 to L = 1. ✓",
            "time": "5 mins"
        },
    ],
    "Advanced Thermodynamics": [
        {
            "difficulty": "Hard",
            "paper": "Paper 2023, Q2",
            "text": "Derive the expression for entropy generation in an irreversible heat engine operating between two thermal reservoirs at temperatures T_H and T_L.",
            "answer": "From Clausius inequality: Sgen = Q_L/T_L - Q_H/T_H ≥ 0. For irreversible: Sgen > 0, efficiency η < 1 - T_L/T_H",
            "time": "15 mins"
        },
        {
            "difficulty": "Medium",
            "paper": "Paper 2022, Q3(b)",
            "text": "Apply the Maxwell relations to derive the Clausius-Clapeyron equation for phase transitions between liquid and vapor states.",
            "answer": "Start from dG = 0 at equilibrium. Using Maxwell relation (∂P/∂T)_V: dP/dT = ΔH_vap / (T·ΔV) ≈ ΔH_vap·P / (RT²)",
            "time": "12 mins"
        },
        {
            "difficulty": "Easy",
            "paper": "Paper 2021, Q5",
            "text": "State the second law of thermodynamics in both Kelvin-Planck and Clausius statements. Show their equivalence.",
            "answer": "Kelvin-Planck: No heat engine can convert all heat to work. Clausius: Heat cannot spontaneously flow from cold to hot. Both are equivalent by contradiction proof.",
            "time": "8 mins"
        },
    ],
    "Electromagnetic Theory": [
        {
            "difficulty": "Hard",
            "paper": "Paper 2023, Q1",
            "text": "Starting from Maxwell's equations in differential form, derive the electromagnetic wave equation for a source-free region. Find the wave speed.",
            "answer": "Take curl of ∇×E = -∂B/∂t, substitute ∇×B = μ₀ε₀∂E/∂t. Get ∇²E = μ₀ε₀∂²E/∂t². Wave speed c = 1/√(μ₀ε₀)",
            "time": "15 mins"
        },
        {
            "difficulty": "Medium",
            "paper": "Paper 2022, Q2(a)",
            "text": "Apply Gauss's law to find the electric field inside and outside a uniformly charged solid sphere of radius R and total charge Q.",
            "answer": "Outside (r>R): E = Q/(4πε₀r²). Inside (r<R): E = Qr/(4πε₀R³). Field increases linearly inside.",
            "time": "10 mins"
        },
    ],
    "Vector Calculus": [
        {
            "difficulty": "Hard",
            "paper": "Paper 2023, Q3",
            "text": "Evaluate the surface integral of F = (x², y², z²) over the closed surface of the unit cube using the Divergence Theorem.",
            "answer": "div F = 2x + 2y + 2z. ∫∫∫div F dV = ∫₀¹∫₀¹∫₀¹(2x+2y+2z)dxdydz = 3.",
            "time": "12 mins"
        },
        {
            "difficulty": "Medium",
            "paper": "Paper 2022, Q4",
            "text": "Use Stokes' theorem to evaluate ∮C F·dr where F = (y, -x, z) and C is the circle x² + y² = 1 in the z = 0 plane.",
            "answer": "curl F = (0, 0, -2). ∫∫(curl F)·dS = -2·π(1)² = -2π.",
            "time": "10 mins"
        },
    ],
}


@router.get("/practice/")
async def get_practice(topic: str = Query(default="General")):
    """Get practice questions for a topic."""

    # Check if we have stored questions from upload analysis
    analysis = analysis_store.get("latest", {})
    stored_questions = analysis.get("questions", [])

    # Filter stored questions by topic if possible
    topic_questions = [
        q for q in stored_questions
        if topic.lower() in q.get("text", "").lower() or
           topic.lower() in q.get("paper", "").lower()
    ]

    # Get from built-in bank
    bank_questions = QUESTION_BANK.get(topic, [])

    # Combine: prefer stored AI questions, supplement with bank
    questions = topic_questions + bank_questions

    # If still empty, generate with Gemini
    if not questions:
        print(f"[Practice] Generating questions for topic: {topic}")
        ai_questions = generate_practice_questions(topic, bank_questions)
        questions = ai_questions if ai_questions else get_generic_questions(topic)

    return {
        "topic": topic,
        "mastery": 72,
        "total_questions": len(questions),
        "questions": questions
    }


def get_generic_questions(topic: str) -> list:
    return [
        {
            "difficulty": "Medium",
            "paper": "AI Generated",
            "text": f"Explain the fundamental principles of {topic} and their applications in modern engineering/science.",
            "answer": f"Review your course notes on {topic}. Focus on core theorems, key equations, and application examples from past papers.",
            "time": "10 mins"
        },
        {
            "difficulty": "Hard",
            "paper": "AI Generated",
            "text": f"Derive a key equation from {topic} from first principles and demonstrate its use in solving a practical problem.",
            "answer": "Start from fundamental definitions, apply mathematical tools (integration, differential equations), arrive at the target equation.",
            "time": "15 mins"
        },
    ]
