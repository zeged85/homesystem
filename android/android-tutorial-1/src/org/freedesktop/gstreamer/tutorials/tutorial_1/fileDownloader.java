package org.freedesktop.gstreamer.tutorials.tutorial_1;

//import android.view.View;
//import android.widget.Toast;

import android.os.Environment;
import android.util.Log;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.PrintWriter;
import java.net.Socket;

public class fileDownloader extends Thread{
    private final Login loginActivity;
    private final String ip;
    private final int port;
    private final long fileSize;


    public fileDownloader(Login loginActivity, String ip, int port, long fileSize) {
        this.loginActivity = loginActivity;
        this.ip = ip;
        this.port = port;
        this.fileSize = fileSize;
    }


        @Override
        public void run() {
            Socket socket = null;
            int bytesRead;
            int current = 0;
            FileOutputStream fos = null;
            BufferedOutputStream bos = null;


            try {
                socket = new Socket(ip, port);
                String name = "wallpaper.jpg";
                File file = new File(
                        Environment.getExternalStorageDirectory(),
                        name);

                if (!file.exists())
                    file.createNewFile();

                byte [] mybytearray  = new byte[(int)(fileSize)];
                //byte[] mybytearray = String.valueOf(fileSize).getBytes();



                //String path = Environment.getExternalStorageDirectory().toString() +"/tmp/wallpaper.jpg";
                //File path = context.getExternalFilesDir(Environment.DIRECTORY_PICTURES);
                InputStream is = socket.getInputStream();
                //FileOutputStream out = new FileOutputStream(file);
                fos = new FileOutputStream(file);
                bos = new BufferedOutputStream(fos);
                bytesRead = is.read(mybytearray,0,mybytearray.length);
                current = bytesRead;


                System.out.println("download start " + mybytearray.length + " bytes left");
                do {
                    System.out.println(mybytearray.length-current);
                    bytesRead =
                            is.read(mybytearray, current, (mybytearray.length-current));
                    if(bytesRead >= 0) current += bytesRead;
                } while(bytesRead > 0);
                System.out.println("download finish");

                bos.write(mybytearray, 0 , current);
                bos.flush();
                String msg = "File " + file
                        + " downloaded (" + current + " bytes read)";
                System.out.println(msg);


//                byte[] temp = new byte[1024];
//                for(int c = is.read(temp,0,1024); c > 0; c = is.read(temp,0,1024)){
//                    out.write(temp,0,c);
//                    Log.d("debug tag", out.toString());
//                }
                Log.d("fileDownloader", msg);


                socket.close();

                loginActivity.runOnUiThread(new Runnable() {

                    @Override
                    public void run() {
                        Toast.makeText(loginActivity,
                                "Finished",
                                Toast.LENGTH_LONG).show();
                    }});

            } catch (IOException e) {

                e.printStackTrace();

                final String eMsg = "Something wrong: " + e.getMessage();
                loginActivity.runOnUiThread(new Runnable() {

                    @Override
                    public void run() {
                        Toast.makeText(loginActivity,
                                eMsg,
                                Toast.LENGTH_LONG).show();
                    }});

            } finally {
                if (fos != null) {
                    try {
                        fos.close();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
                if (bos != null) {
                    try {
                        bos.close();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }

                if(socket != null){
                    try {
                        socket.close();
                    } catch (IOException e) {
                        // TODO Auto-generated catch block
                        e.printStackTrace();
                    }
                }

            }
        }





    public static byte[] longToByteArray(long data) {
        return new byte[] {
                (byte)((data >> 56) & 0xff),
                (byte)((data >> 48) & 0xff),
                (byte)((data >> 40) & 0xff),
                (byte)((data >> 32) & 0xff),
                (byte)((data >> 24) & 0xff),
                (byte)((data >> 16) & 0xff),
                (byte)((data >> 8 ) & 0xff),
                (byte)((data >> 0) & 0xff),
        };
    }



}
