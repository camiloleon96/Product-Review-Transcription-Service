from fastapi import HTTPException

def enqueue_transcription_task(celery_app, video_id, video_url):
    try:
        print(f"[QUEUE] Enqueued transcription task for video_id={video_id}")
        celery_app.send_task("celery_worker.transcribe_video", args=[video_id, video_url])
    except Exception as e:
        print(f"[ERROR] Failed to enqueue transcription task: {e}")
        raise HTTPException(status_code=500, detail="Failed to enqueue transcription task")