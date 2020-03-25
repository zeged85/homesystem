package org.freedesktop.gstreamer.tutorials.tutorial_1;

import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

//ref: https://www.tutorialspoint.com/sending-and-receiving-data-with-sockets-in-android



public class Login extends AppCompatActivity {

    //private TcpClient mTcpClient;
    private String IP;
    private Integer PORT;
    private ProgressBar progressBar;
    private AsyncTask timer;
    private ProgressBar progressBar;

    private Thread Thread1 = null;
    private Thread2 runningThread = null;

    private Socket socket;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);


        setButton1();
        setButton2();
        setButton3();
/*
        if (savedInstanceState != null) {
            gstArray.is_playing_desired = savedInstanceState.getBoolean("playing");
            Log.i ("myLogin", "Activity created. Saved state is playing:" + gstArray.is_playing_desired);

//            gstArray2.is_playing_desired = savedInstanceState.getBoolean("playing2");
//            Log.i ("GStreamer", "Activity created. Saved state is playing2:" + gstArray2.is_playing_desired);
        } else {
            gstArray.is_playing_desired = false;
            Log.i ("myLogin", "Activity created. There is no saved state, playing: false");

//            gstArray2.is_playing_desired = false;
//            Log.i ("GStreamer", "Activity created. There is no saved state, playing2: false");
        }
*/
    }


    protected void onSaveInstanceState (Bundle outState) {
       // Log.d ("GStreamer", "Saving state, playing:" + gstArray.is_playing_desired);
        //outState.putBoolean("playing", gstArray.is_playing_desired);

//        Log.d ("GStreamer", "Saving state, playing2:" + gstArray2.is_playing_desired);
//        outState.putBoolean("playing2", gstArray2.is_playing_desired);
    }

public void setButton3(){
    findViewById(R.id.ping_btn).setOnClickListener(new View.OnClickListener() {
        @Override
        public void onClick(View view) {
            System.out.println("sending ping to server");
            //new Thread(new Thread3("ping")).start();


            JSONObject postData = new JSONObject();
            try{
                postData.put("ID", 1234);
                postData.put("type", "response");
                postData.put("text", "hello\n");

                postData.put("type2", "command");
                postData.put("target", "home0/room2/light1/");
                postData.put("payload", "ON");
            } catch (JSONException e){
                e.printStackTrace();
            }

            new Thread(new Thread3(postData.toString())).start();

        }
    });
}

public void setButton2(){
        findViewById(R.id.logout_btn).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (Thread1 != null){
                    System.out.println("Thread is not null");
                }
                else{
                    System.out.println("Thread is null");
                }
                if (runningThread != null){
                    System.out.println("Shutting down");
                    runningThread.shutdown();
                }
            }
        });
}

    public void setButton1(){
        findViewById(R.id.login_btn).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                //IP
                EditText ip_et = (EditText) findViewById(R.id.ip_txt);
                IP = ip_et.getText().toString();

                //PORT
                EditText port_et = (EditText)findViewById(R.id.port_txt);
                PORT = Integer.parseInt(port_et.getText() .toString());



//                String login_msg = "trying to login to " + IP + ":" + PORT;
//                Toast.makeText(Login.this,login_msg , Toast.LENGTH_LONG).show();



                Thread1 = new Thread(new Thread1());
                Thread1.start();


                progressBar = (ProgressBar)findViewById(R.id.progressBar);
                //progressBar.setVisibility(View.VISIBLE);
                showProgressbar();


//                Intent intent = new Intent(Login.this, Controller.class);
//                startActivity(intent);
//




            }
        });
    }




    private PrintWriter output;
    private BufferedReader input;
    class Thread1 implements Runnable {
        public void run() {
            System.out.println("Thread1 started");
            //Socket socket;
            System.out.println("trying to connect to " + IP + " Port: " + PORT);
            try {
                socket = new Socket(IP, PORT);
                output = new PrintWriter(socket.getOutputStream());
                input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
//                        tvMessages.setText("Connected\n");
                        System.out.println("Connected!");
                        String login_msg = "Connected!";

                        progressBar.setVisibility(View.INVISIBLE);
                        Toast.makeText(Login.this,login_msg , Toast.LENGTH_LONG).show();
                    }
                });
                runningThread = new Thread2();
                new Thread(runningThread).start();
                //Thread2.start();

            } catch (IOException e) {
                e.printStackTrace();
            }
            System.out.println("Thread1 finished");
        }
    }



    class Thread2 implements Runnable {
        private volatile boolean exit = false;
        @Override
        public void run() {
            System.out.println("Thread2 started");
            while (!exit) {
                try {
                    final String message = input.readLine();
                    System.out.println(message);
                    if (message != null) {
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
//                                tvMessages.append("server: " + message + "\n");
                                String login_msg = message;
                                Toast.makeText(Login.this,login_msg , Toast.LENGTH_LONG).show();


                                try {
                                    JSONObject data = new JSONObject(message);

                                    try{
                                        String ter = data.getString("terminal");
                                    } catch (JSONException e) {
                                        System.out.println("terminal not found");
                                        e.printStackTrace();
                                    }



                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }

                            }
                        });
                    } else {
                        Thread1 = new Thread(new Thread1());
                        Thread1.start();
                        return;
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
                System.out.println("Thread2 finished");
            }
        }
        //@Override
        public void shutdown(){
            System.out.println("Shutting Down");
            exit = true;
            if (socket != null){
                try {
                    socket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

    }




    class Thread3 implements Runnable {
        private String message;
        Thread3(String message) {
            System.out.println("Thread3 created");
            this.message = message;
        }
        @Override
        public void run() {
            System.out.println("Thread3 started");
            output.write(message);
            output.flush();
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
//                    tvMessages.append("client: " + message + "\n");
//                    etMessage.setText("");
                    //String login_msg = message;
                    //Toast.makeText(Login.this,login_msg , Toast.LENGTH_LONG).show();
                }
            });
            System.out.println("Thread3 finished");
        }
    }






}