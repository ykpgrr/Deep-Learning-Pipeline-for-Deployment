import org.json.simple.JSONObject;

public abstract class RequestStrategy {
    private RequestInfo info;

    public RequestStrategy() {
        this.info = null;
    }

    JSONObject getRequest(){
        if (info != null) {
            RequestBuilder builder = new RequestBuilder().addValues(
                    "requestId", info.getRequestID(),
                    "userId", info.getUserID(),
                    "ts", info.getTs(),
                    "interval", new RequestBuilder().addValues(
                            "start", info.getStart(),
                            "end", info.getEnd()).build(),
                    "path", info.getPath(),
                    "source", info.getSource(),
                    "analyse_type", info.getAnalyseType());
            return builder.build();
        }

        System.err.println("RequestInfo = null");

        return null;
    }

    public abstract String getSourceType();

    public abstract String getAddress();

    public void setInfo(RequestInfo info) {
        this.info = info;
    }

    public RequestInfo getInfo() {
        return info;
    }
}
