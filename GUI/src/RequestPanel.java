
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class RequestPanel extends JPanel implements ActionListener {
    private static RequestPanel instance = null;

    private JPanel mainPanel;
    private JFileChooser fileChooser;
    private JComboBox sourceTypeComboBox;
    private JComboBox analyzeTypeComboBox;
    private JLabel addressLabel;
    private JButton requestButton;
    private NumberField start;
    private NumberField end;
    private JTextField userIdTextField;
    private JLabel requestIdLabel;

    public static RequestPanel getInstance() {
        if (instance == null)
            instance = new RequestPanel();
        return instance;
    }

    private RequestPanel() {
        create();
    }

    private void create() {
        fileChooser = new JFileChooser();
        mainPanel = new JPanel();
        mainPanel.setLayout(new GridLayout(0, 2));

        mainPanel.add(new JLabel("Request Id:"));
        requestIdLabel = new JLabel("1000");
        mainPanel.add(requestIdLabel);

        mainPanel.add(new JLabel("User Id:"));
        userIdTextField = new JTextField();
        mainPanel.add(userIdTextField);

        mainPanel.add(new JLabel("Source Type:"));
        RequestStrategy[] strategies = {new LocalVideoFileStrategy(), new S3VideoStrategy(), new LocalImageFolderStrategy()};
        sourceTypeComboBox = new JComboBox(strategies);
        sourceTypeComboBox.setSelectedIndex(-1);
        sourceTypeComboBox.addActionListener(this);
        mainPanel.add(sourceTypeComboBox);

        mainPanel.add(new JLabel("Analyze Type:"));
        analyzeTypeComboBox = new JComboBox();
        analyzeTypeComboBox.addItem("two_model");
        analyzeTypeComboBox.addItem("three_model");
        analyzeTypeComboBox.setSelectedIndex(-1);
        mainPanel.add(analyzeTypeComboBox);

        mainPanel.add(new JLabel("Interval:"));
        start = new NumberField(false, true);
        end = new NumberField(false, true);
        JPanel textFieldPanel = new JPanel();
        textFieldPanel.setLayout(new GridLayout(1, 4));
        textFieldPanel.add(new JLabel("start:"));
        textFieldPanel.add(start);
        textFieldPanel.add(new JLabel("end:"));
        textFieldPanel.add(end);
        mainPanel.add(textFieldPanel);

        addressLabel = new JLabel("Address:");
        requestButton = new JButton("Request");
        requestButton.addActionListener(this);
        mainPanel.add(addressLabel);
        mainPanel.add(requestButton);

        setLayout(new BorderLayout());
        add(mainPanel, BorderLayout.NORTH);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == requestButton && checkFields()) {

            int requestID = Integer.parseInt(getRequestIdLabel().getText());
            String userID = getUserIdTextField().getText();
            String source = ((RequestStrategy) sourceTypeComboBox.getSelectedItem()).getSourceType();
            String analyseType = getAnalyzeType();
            float[] interval = getInterval();
            float start = interval[0];
            float end = interval[1];
            String path = getAddressLabel().getText();
            int ts = (int) System.currentTimeMillis();
            RequestInfo info = new RequestInfo(requestID, userID, source, analyseType, start, end, path, ts);
            RequestStrategy strategy = (RequestStrategy) sourceTypeComboBox.getSelectedItem();
            strategy.setInfo(info);
            ResponsePanel responsePanel = new ResponsePanel(strategy.getRequest(), info);
            InitialFrame.getInstance().getTabbedPane().addTab(("" + responsePanel.getRequestID()), responsePanel);
            requestIdLabel.setText("" + (Integer.parseInt(requestIdLabel.getText()) + 1));
            InitialFrame.getInstance().getTabbedPane().updateUI();
        }

        if (e.getSource() == sourceTypeComboBox) {
            RequestStrategy strategy = (RequestStrategy) sourceTypeComboBox.getSelectedItem();
            String address = strategy.getAddress();
            if (address != null)
                addressLabel.setText(address);

        }
    }

    private boolean checkFields() {
        return !start.getText().isEmpty() && !end.getText().isEmpty() && !userIdTextField.getText().isEmpty();
    }
    public JLabel getRequestIdLabel() {
        return requestIdLabel;
    }

    public JTextField getUserIdTextField() {
        return userIdTextField;
    }

    public String getAnalyzeType() {
        return (String) analyzeTypeComboBox.getSelectedItem();
    }

    public JLabel getAddressLabel() {
        return addressLabel;
    }

    public float[] getInterval() {
        float[] interval = { Float.parseFloat(start.getText()), Float.parseFloat(end.getText()) };

        return interval;
    }
}
