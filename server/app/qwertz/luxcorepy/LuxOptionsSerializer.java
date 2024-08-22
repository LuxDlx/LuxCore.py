package app.qwertz.luxcorepy;

import java.io.*;
import java.util.Random;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.sillysoft.lux.BoardFile;
import com.sillysoft.lux.CardSequence;
import com.sillysoft.lux.ContinentSequence;
import com.sillysoft.lux.LuxOptions;


public class LuxOptionsSerializer {
    public static void main(String[] args) throws IOException {
        if (args.length != 1) {
            System.err.println("Usage: java LuxOptionsSerializer <input-json-file>");
            System.exit(1);
        }

        String inputFilePath = args[0];
        Gson gson = new GsonBuilder().create();

        try (Reader reader = new FileReader(inputFilePath)) {
            LuxOptions options = gson.fromJson(reader, LuxOptions.class);

            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ObjectOutputStream oos = new ObjectOutputStream(baos);
            oos.writeObject(options);
            oos.close();

            byte[] serializedData = baos.toByteArray();
            // Write to file
            try (FileOutputStream fos = new FileOutputStream("luxoptions.ser")) {
                fos.write(serializedData);
            }
            System.out.println("Serialized data written to luxoptions.ser");
        }
    }
}
