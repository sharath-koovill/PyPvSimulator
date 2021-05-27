import asyncio
from orchestrator import consume


def main():
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(consume())
        loop.run_forever()
    except KeyboardInterrupt:
        print("KeyBoard Exit after pressing CTRL+C")
    finally:
        loop.close()


if __name__ == "__main__":
    print(" [*] Waiting for messages. To exit press CTRL+C")
    main()