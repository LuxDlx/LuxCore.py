package app.qwertz.luxcorepy;

import java.io.*;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.sillysoft.lux.BoardFile;
import com.sillysoft.lux.CardSequence;
import com.sillysoft.lux.ContinentSequence;
import com.sillysoft.lux.LuxOptions;

public class LuxOptionsDeserializer {
    public static void main(String[] args) throws IOException {
        if (args.length != 1) {
            System.err.println("Usage: java LuxOptionsDeserializer <input-ser-file>");
            System.exit(1);
        }
        try {
            String inputFilePath = args[0];
            // Step 1: Deserialize the object from a file
            FileInputStream fileIn = new FileInputStream(inputFilePath); // Path to your serialized file
            ObjectInputStream in = new ObjectInputStream(fileIn);

            // Deserialize the object
            LuxOptions options = (LuxOptions) in.readObject();

            in.close();
            fileIn.close();

            // Step 2: Convert the deserialized object to JSON
            Gson gson = new GsonBuilder().setPrettyPrinting().create();
            String json = gson.toJson(options);

            // Step 3: Write the JSON string to a file
            try (FileWriter writer = new FileWriter("lux_options.json")) { // Specify the output file name
                writer.write(json);
                System.out.println("LuxOptions saved to luxoptions.json");
            }

        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}