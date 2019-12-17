import org.json.simple.JSONObject;

import javax.swing.*;

public class ResponsePanel extends JPanel implements Observer {
    private RequestInfo info;
    private JSONObject response;

    public ResponsePanel(JSONObject request, RequestInfo info) {
        this.info = info;
        sendRequest(request);

        // TODO Display the response
    }

    private void sendRequest(JSONObject request) {
        JSONObject response = Server.getInstance().sendRequest(request, info.getRequestID());

        // TODO Using response1
    }

    @Override
    public void getResponse(JSONObject request) {
        // TODO Implement GUI with this response JSON
    }

    public int getRequestID() {
        return info.getRequestID();
    }
}