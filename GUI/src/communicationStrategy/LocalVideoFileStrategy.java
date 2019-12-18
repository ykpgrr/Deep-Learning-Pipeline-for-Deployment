import javax.swing.*;

public class LocalVideoFileStrategy extends RequestStrategy{
    @Override
    public String getSourceType() {
        return "Video/Local";
    }

    @Override
    public String toString() {
        return "Local Video";
    }

    @Override
    public String getAddress() {
        JFileChooser fileChooser = new JFileChooser();

        fileChooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
        if (fileChooser.showOpenDialog(RequestPanel.getInstance()) == JFileChooser.APPROVE_OPTION) {
            return fileChooser.getSelectedFile().toString();
        }

        return null;
    }
}
