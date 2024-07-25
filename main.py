import time
import handler_users_messages


def main():
    """
    Run the handler_users_messages.handle_response_data() function for an hour, then pause for 30 minutes.
    
    This function runs the handler_users_messages.handle_response_data() function in a continuous loop. 
    After running for an hour, it pauses for 30 minutes before resuming the execution of the function.

    Args:
        None
        
    Returns:
        None
    """
    while True:
        print(handler_users_messages.handle_response_data())
        time.sleep(30 * 60)


if __name__ == "__main__":
    main()