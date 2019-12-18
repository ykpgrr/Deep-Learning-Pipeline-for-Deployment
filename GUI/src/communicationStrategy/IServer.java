import org.json.simple.JSONObject;

public interface IServer {
    JSONObject sendRequest(JSONObject request, int requestID, ResponsePanel panel);
    void wait(int requestID);
    void remove(int requestID);
}
