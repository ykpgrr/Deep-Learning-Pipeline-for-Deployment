package communicationStrategy;

import org.apache.http.HttpClientConnection;
import org.apache.http.client.HttpClient;
import org.apache.http.params.HttpParams;
import org.apache.http.HttpResponse;
import org.json.simple.JSONObject;
import org.apache.http.impl.client.*;
import org.apache.http.client.methods.*;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import javax.net.ssl.HttpsURLConnection;

public class Client {
    private static final String ADDRESS = "http://localhost:5202/cs550_request";
    private URL url;
    private JSONObject request;
    HttpURLConnection connection;

    public Client(JSONObject request) {
        this.request = request;

    }

    public JSONObject sendRequest() {
        try {
            this.url = new URL(ADDRESS);
            this.connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json; utf-8");
            connection.setRequestProperty("Secret-Key", "0aa43794cd96054e10ecb2df0cf01d0d");
            connection.setDoOutput(true);

            //request.put("Secret-Key", "0aa43794cd96054e10ecb2df0cf01d0d");
            String jsonInputString = request.toJSONString();

            OutputStream os = connection.getOutputStream();
            byte[] input = jsonInputString.getBytes("utf-8");
            os.write(input, 0, input.length);

            os.close();

            BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream(), "utf-8"));

            StringBuilder response = new StringBuilder();
            String responseLine = null;
            while ((responseLine = br.readLine()) != null) {
                response.append(responseLine.trim());
            }

            JSONParser parser = new JSONParser();
            JSONObject responseJSON = (JSONObject) parser.parse(response.toString());

            br.close();
            connection.disconnect();

            return responseJSON;

        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }

        if (connection != null)
            connection.disconnect();

        return null;
    }
}
