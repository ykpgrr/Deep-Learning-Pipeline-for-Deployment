import communicationStrategy.Types;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class RequestPanel extends JPanel implements ActionListener {
    private static RequestPanel instance = null;

    private JPanel mainPanel;
    private JFileChooser fileChooser;
    private JComboBox requestTypeComboBox;
    private JComboBox analyzeTypeComboBox;
    private JLabel addressLabel;
    private JButton requestButton;
    private NumberField start;
    private NumberField end;
    private JTextField userTextfield;
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
        userTextfield = new JTextField();
        mainPanel.add(userTextfield);

        mainPanel.add(new JLabel("Request Type:"));
        requestTypeComboBox = new JComboBox(Types.values());
        requestTypeComboBox.setSelectedIndex(-1);
        requestTypeComboBox.addActionListener(this);
        mainPanel.add(requestTypeComboBox);

        mainPanel.add(new JLabel("Analyze Type:"));
        analyzeTypeComboBox = new JComboBox();
        analyzeTypeComboBox.addItem("two_model");
        analyzeTypeComboBox.addItem("three_model");
        analyzeTypeComboBox.setSelectedIndex(-1);
        mainPanel.add(analyzeTypeComboBox);

        mainPanel.add(new JLabel("Interval"));
        start = new NumberField(false, true);
        end = new NumberField(false, true);
        JPanel textFieldPanel = new JPanel();
        textFieldPanel.setLayout(new GridLayout(1, 4));
        textFieldPanel.add(new JLabel("start"));
        textFieldPanel.add(start);
        textFieldPanel.add(new JLabel("end"));
        textFieldPanel.add(end);
        mainPanel.add(textFieldPanel);

        addressLabel = new JLabel("Address");
        requestButton = new JButton("Request");
        requestButton.addActionListener(this);
        mainPanel.add(addressLabel);
        mainPanel.add(requestButton);

        setLayout(new BorderLayout());
        add(mainPanel, BorderLayout.NORTH);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if(e.getSource() == requestButton && checkFields()) {

            ResponsePanel responsePanel = new ResponsePanel((Types) requestTypeComboBox.getSelectedItem());
            InitialFrame.getInstance().getTabbedPane().addTab(("" + responsePanel.getRequestID()), responsePanel);
            requestIdLabel.setText("" + (Integer.parseInt(requestIdLabel.getText()) + 1));
            InitialFrame.getInstance().getTabbedPane().updateUI();
        }

        if(e.getSource() == requestTypeComboBox) {
            Types type = (Types) requestTypeComboBox.getSelectedItem();
            String address = "";
            switch (type) {
                case LocalVideo:
                    fileChooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
                    if(fileChooser.showOpenDialog(mainPanel)== JFileChooser.APPROVE_OPTION){
                        address = fileChooser.getSelectedFile().toString();
                        addressLabel.setText(address);
                        mainPanel.updateUI();
                    }
                case S3Video:
                    break;
                case LocalImageFolder:
                    fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
                    if(fileChooser.showOpenDialog(mainPanel)== JFileChooser.APPROVE_OPTION){
                        address = fileChooser.getSelectedFile().toString();
                        addressLabel.setText(address);
                        mainPanel.updateUI();
                    }
                default:
                    break;
            }
        }
    }

    private boolean checkFields() {
        if (!start.getText().isEmpty() && !end.getText().isEmpty() && !userTextfield.getText().isEmpty())
            return true;
        return false;
    }
    public JLabel getRequestIdLabel() {
        return requestIdLabel;
    }

    public JTextField getUserTextfield() {
        return userTextfield;
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
