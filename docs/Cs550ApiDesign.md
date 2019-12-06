# API Design
## Incoming Request for deeplearning pipeline
> Requests for deep learning pipeline will be sent by Client (GUI / basic web application).<br/>
> An ID (`request_id`) will be formed for each request and sent with request<br/>
> Requests will be POST requests and parameters are defined below
> Answers to the POST request will mention status of the request. <br/>
When the DL analysis is complete analysis results will be sent by the DL server to client. <br/>

### Cs550 Request
Incoming POST request for DL pipeline:
```
{
    "requestId": 1000,
    "userId": "yakup",
    "ts": 1100, //current time stamp
    "interval": { //in seconds
        "start": 0.00,
        "end": 1.0
    },
    "source": "Video/Local", //Source type. Video-Image/S3-Local-Folder
    "path": "/tests/test_data/videos/test_video_single.mp4" //"s3_video_link or Local Path"
    "analyse_type": "two_model" // "two_model" or "three_model"
}
```
response of this POST request: <br/>
```
400, "Bad Request"
401, "Authentication failed"
201, "Accepted"
```

### Cs550 Response
outgoing POST request from DL pipeline:
```
{
    "requestId": 1000,
    "userId": "yakup",
    "timestamp": 1200, //current time stamp
    "status": "Done", // "Failed" or "Done"
    "cs550Result": {
                    '0.000': 'results',
                    '0.040': 'results',
                    '0.080': 'results',
                    '0.120': 'results',
                    '0.160': 'results',
                    '0.200': 'results',
                    '0.240': 'results'
                    } // 'key': time of the video, 'value': results of that time
}
```
response of this POST request: <br/>
```
20x, "Accepted"
50x, "Failed"
```
