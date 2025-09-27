import asyncio
import websockets
import json
import time
from utils import load_students, sort_students, memory_usage

INPUT_FILE = "students.csv"


async def send_data():
    print("[CLIENT] Starting client...")

    # Load
    students, load_time = load_students(INPUT_FILE)

    # Sort
    students, sort_time = sort_students(students, "name")

    # Prepare data
    data = [s.to_dict() for s in students]
    payload = json.dumps(data)
    print("[CLIENT] Data prepared for sending.")

    # Send to server
    uri = "ws://localhost:8765"
    start_transmit = time.perf_counter()
    async with websockets.connect(uri) as websocket:
        print("[CLIENT] Connected to server.")
        await websocket.send(payload)
        print("[CLIENT] Data sent to server.")

        # Wait for acknowledgement
        ack = await websocket.recv()
        print("[CLIENT] Server says:", ack)
    transmit_time = time.perf_counter() - start_transmit

    # Memory usage
    mem_used = memory_usage()

    # Performance Summary
    print("\n--- CLIENT PERFORMANCE SUMMARY ---")
    print(f"Records sent: {len(students)}")
    print(f"File load time: {load_time:.6f} s")
    print(f"Sort time: {sort_time:.6f} s")
    print(f"Transmit time: {transmit_time:.6f} s")
    print(f"Memory usage: {mem_used:.2f} MB")
    print("----------------------------------")


asyncio.run(send_data())
