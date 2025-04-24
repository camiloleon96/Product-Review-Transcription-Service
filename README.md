# Product-Review-Transcription-Service

To keep track of the development process and decisions, I created a daily dev log in documentation/development_logs. It’s basically a quick way to organize my thoughts, kind of like what I’d write in my notebook. It also includes tasks.

# General description

## High-level design

<img src="./documentation/diagrams/hld.png" alt="High-level Design" width="500"/>

# Intructions

1. **Build and Launch:**

   - Build and launch the Docker Compose file.

2. **Access OpenAPI Documentation:**

   - Visit [http://localhost:8001/docs](http://localhost:8001/docs) to explore the OpenAPI documentation, which includes examples ready to use.

3. **Request a transcription:**

   - Use the `POST` method on `api/video/transcribe` to request a transcription. Refer to the provided example for guidance.

4. **Get a transcription:**

   - Use the `POST` method on `api/video/transcription` and add the video_id to get the transcription with the metadata.

5. **Access the Flower Dashboard:**

   <img src="./docs/flower_dashboard.png" alt="High-level Design" width="700"/>

   - Visit [http://localhost:5556](http://localhost:5556) to access the Flower dashboard. Here, you can monitor the status of the worker and the state of the events a.k.a. tasks (transcriptions).
