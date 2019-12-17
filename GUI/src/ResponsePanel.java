import org.json.simple.JSONObject;

import javax.swing.*;

public class ResponsePanel extends JPanel {
    private RequestInfo info;
    private JSONObject response;

    public ResponsePanel(JSONObject request, RequestInfo info) {
        this.info = info;
        sendRequest(request);

        // TODO Display the response
    }

    private void sendRequest(JSONObject request) {
        Runnable run = new Runnable() {
            @Override
            public void run() {
                Client client = new Client(request);
                response = client.sendRequest();

                JOptionPane.showMessageDialog(null, response.toJSONString());
            }
        };
        Thread thread = new Thread(run);
        thread.start();
    }

    public int getRequestID() {
        return info.getRequestID();
    }
}