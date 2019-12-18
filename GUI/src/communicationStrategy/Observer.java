import org.json.simple.JSONObject;

public interface Observer {
    void getResponse(JSONObject request);
}
