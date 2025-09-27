import asyncio
import websockets
import json
import time
from utils import save_students, memory_usage
from student import Student

OUTPUT_FILE = "output.csv"


async def handle_connection(websocket):
    print("[SERVER] Client connected. Waiting for data...")

    # Receive data
    start_receive = time.perf_counter()
    data = await websocket.recv()
    receive_time = time.perf_counter() - start_receive
    print(f"[SERVER] Data received from client in {receive_time:.6f} seconds.")

    students_list = json.loads(data)
    students = [Student.from_dict(s) for s in students_list]

    save_time = save_students(OUTPUT_FILE, students)

    mem_used = memory_usage()

    # Send acknowledgements
    ack = {
        "status": "ok",
        "records_received": len(students),
        "receive_time_s": round(receive_time, 6),
        "save_time_s": round(save_time, 6),
        "memory_mb": round(mem_used, 2)
    }
    await websocket.send(json.dumps(ack))
    print("[SERVER] Acknowledgement sent to client.")

    print("\n--- SERVER PERFORMANCE SUMMARY ---")
    print(f"Records saved: {len(students)}")
    print(f"Receive time: {receive_time:.6f} s")
    print(f"Save time: {save_time:.6f} s")
    print(f"Memory usage: {mem_used:.2f} MB")
    print("----------------------------------\n")


async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("[SERVER] Server started at ws://localhost:8765")
        await asyncio.Future()  # keep running


asyncio.run(main())
