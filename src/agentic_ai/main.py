from dotenv import load_dotenv

from agentic_ai.agent import AgentController


def main():

    load_dotenv()

    agent = AgentController(max_steps=5)

    user_message = (
        "My order #4821 has not arrived. Please investigate and tell me what happened."
    )

    result = agent.run(user_message)

    print("\n========== FINAL RESPONSE ==========")
    print(result)


if __name__ == "__main__":
    main()
