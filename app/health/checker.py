import time
import httpx

async def check_service(url:str):
    start=time.time()
    try:
        async with httpx.AsyncClient(timeout=10) as client:
         response=await client.get(url)
        response_time=int((time.time()-start)*1000) 
        
        if response.status_code < 400 :
            return {
                "status":"UP",
                "status_code":response.status_code,
                "response_time":response_time,
                "error":None
            }
        return{
            "status":"DOWN",
            "status_code":response.status_code,
            "response_time":response_time,
            "error":f"HTTP {response.error}"
        }     
    except Exception as e:
        return {
            "status":"DOWN",
            "response_time":None,
            "error":str(e)
        }     