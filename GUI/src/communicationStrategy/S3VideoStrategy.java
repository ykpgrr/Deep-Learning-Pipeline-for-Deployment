
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
        return null;
    }
}
