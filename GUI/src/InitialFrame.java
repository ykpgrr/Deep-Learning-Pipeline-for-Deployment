import javax.swing.*;
import java.awt.*;

public class InitialFrame extends JFrame {
    private static InitialFrame instance = null;
    private final static int height = 600, width = 600;

    private JTabbedPane tabbedPane;
    private RequestPanel requestPanel;
    //private ResponsePanel ResponsePanel;

    private InitialFrame() {
        setLocation(100, 100);
        setSize(width, height);
        setLayout(new BorderLayout());

        tabbedPane = new JTabbedPane();
        requestPanel = RequestPanel.getInstance();
        tabbedPane.addTab("Create Request", requestPanel);
        add(tabbedPane, BorderLayout.CENTER);
        setVisible(true);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
    }

    public static InitialFrame getInstance() {
        if (instance == null)
            instance = new InitialFrame();
        return instance;
    }

    public JTabbedPane getTabbedPane() {
        return tabbedPane;
    }
}
