import javax.swing.*;

public class LocalImageFolderStrategy extends RequestStrategy {
    @Override
    public String getSourceType() {
        return "Image/Local";
    }

    @Override
    public String toString() {
        return "Local Image Folder";
    }

    @Override
    public String getAddress() {
        JFileChooser fileChooser = new JFileChooser();

        fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        if (fileChooser.showOpenDialog(RequestPanel.getInstance()) == JFileChooser.APPROVE_OPTION) {
            return fileChooser.getSelectedFile().toString();
        }

        return null;
    }
}
