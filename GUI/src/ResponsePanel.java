import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import javax.swing.*;
import java.awt.*;

public class ResponsePanel extends JPanel implements Observer {
    private RequestInfo info;
    private JPanel upperPanel;
    private JLabel requestIdLabel;
    private JLabel userIdLabel;
    private JLabel timeStampLabel;
    private JLabel statusLabel;
    private JPanel centerPanel;


    public ResponsePanel(JSONObject request, RequestInfo info) {
        this.info = info;
        create();
        sendRequest(request);
    }

    private void create() {
        upperPanel = new JPanel();
        upperPanel.setLayout(new GridLayout(0, 2));
        upperPanel.add(new JLabel("Request Id:"));
        requestIdLabel = new JLabel(Integer.toString(info.getRequestID()));
        upperPanel.add(requestIdLabel);
        upperPanel.add(new JLabel("User Id:"));
        userIdLabel = new JLabel(info.getUserID());
        upperPanel.add(userIdLabel);
        upperPanel.add(new JLabel("Time Stamp:"));
        timeStampLabel = new JLabel(Integer.toString(info.getTs()));
        upperPanel.add(timeStampLabel);
        upperPanel.add(new JLabel("Status:"));
        statusLabel = new JLabel("Waiting");
        upperPanel.add(statusLabel);

        centerPanel = new JPanel();
        centerPanel.setLayout(new BorderLayout());
        centerPanel.add(new JLabel("Results:"), BorderLayout.NORTH);

        setLayout(new BorderLayout());
        add(upperPanel, BorderLayout.NORTH);
        add(centerPanel, BorderLayout.CENTER);

    }

    private void sendRequest(JSONObject request) {
        JSONObject response = Server.getInstance().sendRequest(request, info.getRequestID(), this);
        statusLabel.setText((String) response.get("jobStatus"));

        Server.getInstance().wait(info.getRequestID());
    }

    @Override
    public void getResponse(JSONObject request) {
        try {
            JSONParser parser = new JSONParser();
            request = (JSONObject) parser.parse("{\n" +
                    "  \"requestId\": 1007,\n" +
                    "  \"userId\": \"yakup\",\n" +
                    "  \"timestamp\": 1576598990.741045,\n" +
                    "  \"status\": \"Done\",\n" +
                    "  \"cs550Result\": {\n" +
                    "    \"0.000\": \"Model2Result\",\n" +
                    "    \"0.040\": \"Model2Result\",\n" +
                    "    \"0.080\": \"Model2Result\",\n" +
                    "    \"0.120\": \"Model2Result\",\n" +
                    "    \"0.160\": \"Model2Result\",\n" +
                    "    \"0.200\": \"Model2Result\",\n" +
                    "    \"0.240\": \"Model2Result\",\n" +
                    "    \"0.280\": \"Model2Result\",\n" +
                    "    \"0.320\": \"Model2Result\",\n" +
                    "    \"0.360\": \"Model2Result\",\n" +
                    "    \"0.400\": \"Model2Result\",\n" +
                    "    \"0.440\": \"Model2Result\",\n" +
                    "    \"0.480\": \"Model2Result\",\n" +
                    "    \"0.520\": \"Model2Result\",\n" +
                    "    \"0.560\": \"Model2Result\",\n" +
                    "    \"0.600\": \"Model2Result\",\n" +
                    "    \"0.640\": \"Model2Result\",\n" +
                    "    \"0.680\": \"Model2Result\",\n" +
                    "    \"0.720\": \"Model2Result\",\n" +
                    "    \"0.760\": \"Model2Result\",\n" +
                    "    \"0.800\": \"Model2Result\",\n" +
                    "    \"0.840\": \"Model2Result\",\n" +
                    "    \"0.880\": \"Model2Result\",\n" +
                    "    \"0.920\": \"Model2Result\",\n" +
                    "    \"0.960\": \"Model2Result\"\n" +
                    "  }}");
        } catch (ParseException e) {
            System.out.println("hata");
        }
        System.out.println("Girdi.");
        requestIdLabel.setText("" + request.get("requestId"));
        userIdLabel.setText("" + request.get("userId"));
        timeStampLabel.setText("" +  request.get("timestamp"));
        requestIdLabel.setText("" +  request.get("status"));
        JSONObject results = (JSONObject) request.get("cs550Result");

        String[] column = {"Time", "Model Type"};
        String[][] data = new String[results.keySet().size()][2];
        Object[] keys = results.keySet().toArray();

        for (int i = 0; i < keys.length; i++) {
            data[i][0] = keys[i].toString();
            data[i][1] = "" + results.get(data[i][0]);
        }
        JTable table = new JTable(data, column);
        JScrollPane scrollPane = new JScrollPane(table);
        centerPanel.add(table.getTableHeader(), BorderLayout.NORTH);
        centerPanel.add(scrollPane, BorderLayout.CENTER);
        centerPanel.updateUI();

    }

    public int getRequestID() {
        return info.getRequestID();
    }
}