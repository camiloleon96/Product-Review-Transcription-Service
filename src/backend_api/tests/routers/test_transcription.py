from unittest.mock import patch
from fastapi.testclient import TestClient
from app.routers.transcription import router

client = TestClient(router)

def test_transcribe_success():
    mock_video_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_url = "http://example.com/video.mp4"

    with patch("app.routers.transcription.add_video_record") as mock_add_video_record, \
         patch("app.routers.transcription.enqueue_transcription_task") as mock_enqueue_task:
        mock_add_video_record.return_value = None
        mock_enqueue_task.return_value = None

        response = client.post("/video/transcribe", json={"url": mock_url})

        assert response.status_code == 202
        assert response.json() == {
            "video_id": mock_video_id,
            "status": "pending",
            "message": "Transcription in progress. Use GET /transcription/{video_id} to check status."
        }

def test_transcribe_db_error():
    mock_url = "http://example.com/video.mp4"

    with patch("app.routers.transcription.add_video_record", side_effect=Exception("DB error")):
        response = client.post("/video/transcribe", json={"url": mock_url})

        assert response.status_code == 500
        assert response.json() == {"detail": "Database error while processing transcription"}

def test_get_transcription_success():
    mock_video_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_transcription = {
        "title": "Test Video",
        "url": "http://example.com/video.mp4",
        "transcription_status": "completed",
        "language": "en",
        "transcribed_text": "This is a test transcription."
    }

    with patch("app.routers.transcription.fetch_video_and_transcription", return_value=mock_transcription):
        response = client.get(f"/video/transcription/{mock_video_id}")

        assert response.status_code == 200
        assert response.json() == {
            "video_id": mock_video_id,
            "title": mock_transcription["title"],
            "url": mock_transcription["url"],
            "status": mock_transcription["transcription_status"],
            "language": mock_transcription["language"],
            "transcription": mock_transcription["transcribed_text"]
        }

def test_get_transcription_not_found():
    mock_video_id = "123e4567-e89b-12d3-a456-426614174000"

    with patch("app.routers.transcription.fetch_video_and_transcription", return_value=None):
        response = client.get(f"/video/transcription/{mock_video_id}")

        assert response.status_code == 404
        assert response.json() == {"detail": "Video not found"}

def test_get_transcription_db_error():
    mock_video_id = "123e4567-e89b-12d3-a456-426614174000"

    with patch("app.routers.transcription.fetch_video_and_transcription", side_effect=Exception("DB error")):
        response = client.get(f"/video/transcription/{mock_video_id}")

        assert response.status_code == 500
        assert response.json() == {"detail": "Database error while fetching transcription"}