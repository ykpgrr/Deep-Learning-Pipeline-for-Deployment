import communicationStrategy.Client;
import communicationStrategy.RequestBuilder;
import communicationStrategy.Types;
import org.json.simple.JSONObject;

import javax.swing.*;

public class ResponsePanel extends JPanel {
    private Types type;
    private String userID, source, path, analyseType;
    private int requestID, ts;
    private float start, end;

    private Thread thread;
    private JSONObject response;

    public ResponsePanel(Types type) {
        this.type = type;
        path = RequestPanel.getInstance().getAddressLabel().getText();
        float[] interval = RequestPanel.getInstance().getInterval();

        start = interval[0];
        end = interval[1];
        analyseType = RequestPanel.getInstance().getAnalyzeType();
        requestID = Integer.parseInt(RequestPanel.getInstance().getRequestIdLabel().getText());
        userID = RequestPanel.getInstance().getUserTextfield().getText();
        ts = (int)System.currentTimeMillis();
        source = getAnalyseType(type);

        sendRequest();

        // TODO Display the response
    }

    private static String getAnalyseType(Types type) {
        switch (type) {
            case LocalImageFolder:
                return "Image" + (char)(47) + "Local";
            case LocalVideo:
                return "Video" + (char)(47) + "Local";
            case S3Video:
                return "Video" + (char)(47) + "S3";
        }

        return "";
    }

    private void sendRequest() {
        Runnable run = new Runnable() {
            @Override
            public void run() {
                JSONObject request = getRequest();
                Client client = new Client(request);
                response = client.sendRequest();


                JOptionPane.showMessageDialog(null, response.toJSONString());
            }
        };

        thread = new Thread(run);
        thread.start();

    }

    public int getRequestID() {
        return requestID;
    }

    private JSONObject getRequest() {
        RequestBuilder builder = new RequestBuilder().addValues("requestId", requestID, "userId", userID, "ts", ts,
                "interval", getInterval(), "path", path, "source", source, "analyse_type", analyseType);

        return builder.build();
    }

    private JSONObject getInterval() {
        return new RequestBuilder().addValues("start", start, "end", end).build();
    }
}