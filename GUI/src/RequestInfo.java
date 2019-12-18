
public class RequestInfo {
    private String userID, source, path, analyseType;
    private int requestID, ts;
    private float start, end;

    public RequestInfo(int requestID, String userID, String source, String analyseType,
    float start, float end, String path, int ts) {
        this.requestID = requestID;
        this.userID = userID;
        this.source = source;
        this.analyseType = analyseType;
        this.start = start;
        this.end = end;
        this.path = path;
        this.ts = ts;
    }

    public int getRequestID() {
        return requestID;
    }

    public String getUserID() {
        return userID;
    }

    public String getSource() {
        return source;
    }

    public String getAnalyseType() {
        return analyseType;
    }

    public float getStart() {
        return start;
    }

    public float getEnd() {
        return end;
    }

    public String getPath() {
        return path;
    }

    public int getTs() {
        return ts;
    }
}
