import javax.swing.*;
import java.awt.*;

public class S3VideoStrategy extends RequestStrategy {
    @Override
    public String getSourceType() {
        return "Video/S3";
    }

    @Override
    public String toString() {
        return "S3 Video";
    }

    @Override
    public String getAddress() {
        String address = JOptionPane.showInputDialog(null, "Enter S3 Video Path");

        if (address == null || address.isEmpty())
            return null;

        return address;
    }
}
