package org.freedesktop.gstreamer.tutorials.tutorial_1;

import android.util.Log;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketException;
import java.net.SocketTimeoutException;

public class TcpClient {

    //https://stackoverflow.com/questions/38162775/really-simple-tcp-client

    public static final String TAG = TcpClient.class.getSimpleName();
    public static String SERVER_IP = "10.0.0.41"; //server IP address
    public static Integer SERVER_PORT = 10006;
    public static final Integer TIMEOUT = 10000;
    public static Socket socket;

    // message to send to the server
    private String mServerMessage;
    // sends message received notifications
    private OnMessageReceived mMessageListener = null;
    // while this is true, the server will continue running
    private boolean mRun = false;
    // used to send messages
    private PrintWriter mBufferOut;
    // used to read messages from the server
    private BufferedReader mBufferIn;

    private Socket socket;


    // status to send to the server
    private String mServerStatus;
    // sends status received notifications
    private OnStatusReceived mStatusListener = null;

//    TcpClient(String ip, Integer port){
//        SERVER_IP=ip;
//        SERVER_PORT=port;
//        System.out.println("in tcpClient const.");
//
//    }


    /**
     * Constructor of the class. OnMessagedReceived listens for the messages received from server
     */
    public TcpClient(String ip, Integer port, OnMessageReceived listener, OnStatusReceived slistener) {
        mMessageListener = listener;
        mStatusListener = slistener;
        SERVER_IP = ip;
        SERVER_PORT = port;
    }

    /**
     * Sends the message entered by client to the server
     *
     * @param message text entered by client
     */
    public void sendMessage(final String message) {
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                if (mBufferOut != null) {
                    Log.d(TAG, "Sending: " + message);
                    mBufferOut.println(message);
                    mBufferOut.flush();
                }
            }
        };
        Thread thread = new Thread(runnable);
        thread.start();
    }

    /**
     * Close the connection and release the members
     */
    public void stopClient() throws IOException {

        mRun = false;

        if (mBufferOut != null) {
            mBufferOut.flush();
            mBufferOut.close();
        }

        mMessageListener = null;
        mBufferIn = null;
        mBufferOut = null;
        mServerMessage = null;
    }

    public void cancel() throws IOException {
        socket.close();
        stopClient();
    }

    public void run() {

        mRun = true;

        try {
            //here you must put your computer's IP address.
            InetAddress serverAddr = InetAddress.getByName(SERVER_IP);

            Log.d("TCP Client", "C: Connecting...");

            //create a socket to make the connection with the server

            InetSocketAddress sockAdr = new InetSocketAddress(SERVER_IP, SERVER_PORT);
            socket = new Socket();
//            Integer timeout = 3000;

            try {
                socket.connect(sockAdr, TIMEOUT);

                System.out.println("I am connected to a server!!");

//                mMessageListener.messageReceived(mServerMessage); //TODO: status listener
                mStatusListener.statusReceived(mServerStatus);


            }
            catch (SocketTimeoutException e){
                System.out.println("server not found yet: timeout");
                if(socket.isConnected()){
//                    disconnect();
                    System.out.println("still connected");
                }
                System.out.println("got disconnected");
                mMessageListener.messageReceived("server was not found after " + TIMEOUT/1000 +" seconds!");
//                connect();
            } catch (SocketException e){
                System.out.println("caught a Socket Exception: maybe Socket is closed? ");
                System.out.println("type: " + e.getClass().getCanonicalName());
                System.out.println("message: " + e.getMessage());
                Log.e("TCP", "S: Error - Socket got closed?", e);

                if (e.getMessage().compareTo("Socket Closed")==0){
                    System.out.println("I recognize that socket is close and i shouhld break op");
                    System.out.println("message ok");
                }

                if (e.getClass().getCanonicalName().compareTo("java.net.SocketException")==0){
                    System.out.println("I recognize that socket is close and i shouhld break op");
                    System.out.println("java.net.SocketException ok");

                    return;
                }
            }


//            Integer timeout = 3500;
//            Socket socket = new Socket(serverAddr, SERVER_PORT, timeout);

            //set timeout
//            socket.setSoTimeout(4);

            try {

                //sendMessage("hello??"); //first send
                //sends the message to the server
                mBufferOut = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);

                //receives the message which the server sends back
                mBufferIn = new BufferedReader(new InputStreamReader(socket.getInputStream()));


                //in this while the client listens for the messages sent by the server
                while (mRun) {

                    mServerMessage = mBufferIn.readLine();

                    if (mServerMessage != null && mMessageListener != null) {
                        //call the method messageReceived from MyActivity class
                        mMessageListener.messageReceived(mServerMessage);
                    }

                }

                Log.d("RESPONSE FROM SERVER", "S: Received Message: '" + mServerMessage + "'");

            } catch (SocketException e){
                System.out.println("catching socket close");
                Log.e("TCP", "S: Error", e);
            } catch (Exception e) {
                Log.e("TCP", "S: Error", e);

            } finally {
                //the socket must be closed. It is not possible to reconnect to this socket
                // after it is closed, which means a new socket instance has to be created.
                socket.close();
            }

        }

        catch (Exception e) {
            Log.e("TCP", "C: Error", e);
        }

    }

    //Declare the interface. The method messageReceived(String message) will must be implemented in the Activity
    //class at on AsyncTask doInBackground
    public interface OnMessageReceived {
        public void messageReceived(String message);

        //here the statusReceived method is implemented
//        void statusReceived(String status);
    }

    public interface OnStatusReceived {
        public void statusReceived(String status);
    }




}
