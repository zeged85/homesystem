package org.freedesktop.gstreamer.tutorials.tutorial_1;

import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Toast;

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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);


        setButton1();

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
            Socket socket;
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
                new Thread(new Thread2()).start();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }



    class Thread2 implements Runnable {
        @Override
        public void run() {
            while (true) {
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
            }
        }
    }




    class Thread3 implements Runnable {
        private String message;
        Thread3(String message) {
            this.message = message;
        }
        @Override
        public void run() {
            output.write(message);
            output.flush();
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
//                    tvMessages.append("client: " + message + "\n");
//                    etMessage.setText("");
                    String login_msg = message;
                    Toast.makeText(Login.this,login_msg , Toast.LENGTH_LONG).show();
                }
            });
        }
    }






}