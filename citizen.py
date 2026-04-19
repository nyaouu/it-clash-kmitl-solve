import asyncio
import aiohttp
import json
import os

async def fetch_citizen(session, citizen_id):
    url = f"http://instance.ctf.it.kmitl.ac.th:4563/api/citizen/{citizen_id}"
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"ID {citizen_id} failed with status: {response.status}")
                return None
    except Exception as e:
        print(f"Error fetching ID {citizen_id}: {e}")
        return None

async def main():
    start_id = 10000
    end_id = 99999
    output_file = "citizens_data.json"
    
    # กำหนดจำนวน concurrent requests (ไม่ควรสูงเกินไปเพื่อป้องกัน server ล่ม)
    sem = asyncio.Semaphore(50) 
    
    async def limited_fetch(session, citizen_id):
        async with sem:
            return await fetch_citizen(session, citizen_id)

    async with aiohttp.ClientSession() as session:
        tasks = [limited_fetch(session, i) for i in range(start_id, end_id + 1)]
        
        print(f"Starting requests for IDs {start_id} to {end_id}...")
        results = await asyncio.gather(*tasks)
        
        # กรองเอาเฉพาะข้อมูลที่ไม่เป็น None
        valid_data = [r for r in results if r is not None]
        
        # บันทึกลงไฟล์ JSON
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(valid_data, f, ensure_ascii=False, indent=2)
            
        print(f"Done! Saved {len(valid_data)} records to {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
