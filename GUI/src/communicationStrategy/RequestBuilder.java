import org.json.simple.JSONObject;

public class RequestBuilder {
    private RequestInfo requestInfo;
    private JSONObject request;

    public RequestBuilder() {
        request = new JSONObject();
    }

    private RequestBuilder(JSONObject request) {
        this.request = request;
    }

    public RequestBuilder addValues(Object ... list) {
        if (list.length % 2 != 0)
            throw new IllegalArgumentException("List length must be even.");

        RequestBuilder builder = new RequestBuilder(request);

        for (int i = 0; i < list.length; i += 2)
            builder = addValue(list[i].toString(), list[i + 1]);

        return builder;
    }

    public RequestBuilder addValue(String name, Object value) {
        RequestBuilder builder = new RequestBuilder(request);

        builder.request.put(name, value);

        return builder;
    }

    public JSONObject build() {
        return request;
    }
}
