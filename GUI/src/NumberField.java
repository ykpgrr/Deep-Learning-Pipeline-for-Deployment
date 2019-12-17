import javax.swing.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

public class NumberField extends JTextField implements KeyListener {
    private boolean isInteger;
    private boolean isPositive;

    public NumberField() {
        addKeyListener(this);
        isInteger = false;
        isPositive = false;
    }

    public NumberField(boolean isInteger) {
        addKeyListener(this);
        this.isInteger = isInteger;
        isPositive = false;
    }

    public NumberField(boolean isInteger, boolean isPositive) {
        addKeyListener(this);
        this.isInteger = isInteger;
        this.isPositive = isPositive;
    }

    @Override
    public void keyTyped(KeyEvent e) {
        if (e.getKeyChar() == '0') {
            String text = getText();

            if (text.length() == 0)
                return;

            if (text.indexOf('0') > -1 && text.indexOf('.') == -1 && Double.parseDouble(text) == 0)
                e.consume();
        }
        else if (!isPositive && e.getKeyChar() == '-') {
            String text = getText();

            if (text.length() > 0) // Only first char can be '-'
                e.consume();
        }
        else if (!isInteger && e.getKeyChar() == '.') {
            String text = getText();
            if (text.indexOf('.') > -1) // Only one '.'
                e.consume();
            else if (text.length() == 0 || text.charAt(text.length() - 1) == '-')
                e.consume();
        }
        else if (e.getKeyChar() < '0' || e.getKeyChar() > '9')
            e.consume();
    }

    @Override
    public void keyPressed(KeyEvent e) {
        ;
    }

    @Override
    public void keyReleased(KeyEvent e) {
        ;
    }

    public double getValueAsDouble() {
        return Double.parseDouble(getText());
    }

    public int getValueAsInteger() {
        return (int) Double.parseDouble(getText());
    }
}
