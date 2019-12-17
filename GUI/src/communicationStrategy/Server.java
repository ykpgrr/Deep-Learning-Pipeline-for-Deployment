import com.sun.net.httpserver.HttpServer;
import org.json.simple.JSONObject;

import java.util.HashMap;

public class Server implements IServer {
    private static Server ourInstance = new Server();

    public static Server getInstance() {
        return ourInstance;
    }


    private HttpServer server;
    private HashMap<Integer, ResponsePanel> panels;

    private Server() {
        panels = new HashMap<>();
    }

    @Override
    public JSONObject sendRequest(JSONObject request, int requestID) {
        return null;
    }

    @Override
    public void remove(int requestID) {

    }
}
