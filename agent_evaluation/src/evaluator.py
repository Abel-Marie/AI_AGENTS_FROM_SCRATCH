import json

def create_eval_config():
    """Creates evaluation configuration with scoring criteria."""
    return {
        "criteria": {
            "tool_trajectory_avg_score": 1.0,  # Perfect tool usage required
            "response_match_score": 0.8,  # 80% text similarity threshold
        }
    }

def create_test_cases():
    """Creates evaluation test cases for the home automation agent."""
    return {
        "eval_set_id": "home_automation_integration_suite",
        "eval_cases": [
            {
                "eval_id": "living_room_light_on",
                "conversation": [
                    {
                        "user_content": {
                            "parts": [
                                {"text": "Please turn on the floor lamp in the living room"}
                            ]
                        },
                        "final_response": {
                            "parts": [
                                {
                                    "text": "Successfully set the floor lamp in the living room to on."
                                }
                            ]
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "set_device_status",
                                    "args": {
                                        "location": "living room",
                                        "device_id": "floor lamp",
                                        "status": "ON",
                                    },
                                }
                            ]
                        },
                    }
                ],
            },
            {
                "eval_id": "kitchen_on_off_sequence",
                "conversation": [
                    {
                        "user_content": {
                            "parts": [{"text": "Switch on the main light in the kitchen."}]
                        },
                        "final_response": {
                            "parts": [
                                {
                                    "text": "Successfully set the main light in the kitchen to on."
                                }
                            ]
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "set_device_status",
                                    "args": {
                                        "location": "kitchen",
                                        "device_id": "main light",
                                        "status": "ON",
                                    },
                                }
                            ]
                        },
                    }
                ],
            },
        ],
    }

def save_eval_config(config, filepath="test_data/test_config.json"):
    """Saves evaluation configuration to file."""
    with open(filepath, "w") as f:
        json.dump(config, f, indent=2)
    print(f"✅ Evaluation configuration saved to {filepath}")

def save_test_cases(test_cases, filepath="test_data/integration.evalset.json"):
    """Saves test cases to file."""
    with open(filepath, "w") as f:
        json.dump(test_cases, f, indent=2)
    print(f"✅ Test cases saved to {filepath}")

def print_eval_summary(config, test_cases):
    """Prints a summary of the evaluation setup."""
    print("\n📊 Evaluation Criteria:")
    for key, value in config["criteria"].items():
        print(f"• {key}: {value}")
    
    print("\n🎯 What this evaluation will catch:")
    print("✅ Incorrect tool usage (wrong device, location, or status)")
    print("✅ Poor response quality and communication")
    print("✅ Deviations from expected behavior patterns")
    
    print("\n🧪 Test scenarios:")
    for case in test_cases["eval_cases"]:
        user_msg = case["conversation"][0]["user_content"]["parts"][0]["text"]
        print(f"• {case['eval_id']}: {user_msg}")
