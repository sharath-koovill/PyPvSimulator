import asyncio
from orchestrator import produce


def main():
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(produce())
        loop.run_forever()
    except KeyboardInterrupt:
        print("KeyBoard Exit after pressing CTRL+C")
    finally:
        loop.close()


if __name__ == "__main__":
    print(" Sending messages. To exit press CTRL+C")
    main()
