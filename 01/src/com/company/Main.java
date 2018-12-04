package com.company;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Vector;

public class Main {

    public static void main(String[] args) {
        String input_file = "input.txt";
        String line;

        try {
            FileReader fr;
            BufferedReader br;
            int x = 0;
            Vector seen = new Vector();
            seen.add(x);
            while (true) {
                fr = new FileReader(input_file);
                br = new BufferedReader(fr);
                while ((line = br.readLine()) != null) {
                    // System.out.println("x: " + x);
                    x = x + Integer.parseInt(line);
                    if (seen.contains(x)) {
                        System.out.println("First frequency your device reaches twice: " + x);
                        return;
                    }
                    seen.add(x);
                }
                br.close();
            }
            // System.out.println("\nFinal x: " + x);
        }
        catch(FileNotFoundException ex) {
            System.out.println("Error: File \"" + input_file + "\" not found.");
        }
        catch (IOException ex) {
            ex.printStackTrace();
        }
    }
}
