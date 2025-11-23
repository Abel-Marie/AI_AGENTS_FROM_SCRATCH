import sqlite3
from google.genai import types
from google.adk.runners import Runner 

async def run_session(
        runner_instance: Runner,
        user_queries: list[str] | str = None,
        session_name: str = "default",
        user_id: str = "default",
        model_name: str = "gemini-2.5-flash-lite",
): 

    """Helper function to manage a complete conversation session."""
    print(f"\n ### Session: {session_name}")

    # Get app name from the Runner
    app_name = runner_instance.app_name
    session_service = runner_instance.session_service

    # Attempt to create a new session or retrieve an existing one
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=user_id, session_id=session_name
        )
    except:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_name
        )

    # Process queries if provided
    if user_queries:
        # Convert single query to list for uniform processing
        if type(user_queries) == str:
            user_queries = [user_queries]

        # Process each query in the list sequentially
        for query in user_queries:
            print(f"\nUser > {query}")

            # Convert the query string to the ADK Content format
            query_content = types.Content(role="user", parts=[types.Part(text=query)])

            # Stream the agent's response asynchronously
            async for event in runner_instance.run_async(
                user_id=user_id, session_id=session.id, new_message=query_content
            ):
                # Check if the event contains valid content
                if event.content and event.content.parts:
                    # Filter out empty or "None" responses before printing
                    for part in event.content.parts:
                        if part.text and part.text != "None":
                            print(f"{model_name} > ", part.text)
    else:
        print("No queries!")

def check_data_in_db(db_path="my_agent_data.db"):
    """Inspects the SQLite database events."""
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            result = cursor.execute(
                "select app_name, session_id, author, content from events"
            )
            print([_[0] for _ in result.description])
            for each in result.fetchall():
                print(each)
    except Exception as e:
        print(f"Error checking DB: {e}")

        