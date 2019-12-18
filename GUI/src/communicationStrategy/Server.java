import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;


import java.net.http.HttpClient;
import java.util.HashMap;

public class Server implements IServer {
    private final static int PORT = 4305;

    private static Server ourInstance = new Server();

    public static Server getInstance() {
        return ourInstance;
    }

    private HttpClient client;
    private HashMap<Integer, ResponsePanel> panels;

    private Server() {
        panels = new HashMap<>();
    }

    public void wait(int requestID) {
        /*
        String request = "{ \"requestId\":" + requestID + "}";

        try {
            JSONParser parser = new JSONParser();
            JSONObject requestJSON = (JSONObject) parser.parse(request);
            Thread thread = new Thread(new Runnable() {
                @Override
                public void run() {
                    Client client = new Client(requestJSON);
                    JSONObject response = client.sendRequest();
                    ResponsePanel panel = panels.get(requestID);

                    panel.getResponse(response);
                }
            });

            thread.start();

        } catch (Exception e) {
            e.printStackTrace();
        }
        */
    }

    @Override
    public JSONObject sendRequest(JSONObject request, int requestID, ResponsePanel panel) {
        panels.put(requestID, panel);

        Client client = new Client(request);

        return client.sendRequest();
    }

    @Override
    public void remove(int requestID) {
        panels.remove(requestID);
    }
}