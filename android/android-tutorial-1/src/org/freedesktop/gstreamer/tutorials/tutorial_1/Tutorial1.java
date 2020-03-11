package org.freedesktop.gstreamer.tutorials.tutorial_1;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import android.view.View.OnClickListener;

import android.view.SurfaceHolder;
import android.view.SurfaceView;

import org.freedesktop.gstreamer.GStreamer;

//import org.freedesktop.gstreamer.tutorials.tutorial_1.GstSingle;




public class Tutorial1 extends Activity implements SurfaceHolder.Callback{
//    private native void nativeInit();     // Initialize native code, build pipeline, etc
//    private native void nativeFinalize(); // Destroy pipeline and shutdown native code
//    private native void nativePlay();     // Set pipeline to PLAYING
//    private native void nativePause();    // Set pipeline to PAUSED
//    private static native boolean nativeClassInit(); // Initialize native class: cache Method IDs for callbacks
//    private native void nativeSurfaceInit(Object surface);
//    private native void nativeSurfaceFinalize();
    private long native_custom_data;      // Native code will use this to keep private data

    private boolean is_playing_desired;   // Whether the user asked to go to PLAYING

    //private native String nativeGetGStreamerInfo();
    // tutorial2

    GstSingle gstArray;

    // Called when the activity is first created.
    @Override
    public void onCreate(Bundle savedInstanceState)
    {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        GstSingle gstSingle = new GstSingle(this);


//        try {
//            GStreamer.init(this);
//        } catch (Exception e) {
//            Toast.makeText(this, e.getMessage(), Toast.LENGTH_LONG).show();
//            this.finish();
//            return;
//        }








//        TextView tv = (TextView)findViewById(R.id.textview_info);
//        tv.setText("Welcome to " + nativeGetGStreamerInfo() + " !");

        gstArray = gstSingle;




        ImageButton play = (ImageButton) this.findViewById(R.id.button_play);
        play.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                gstArray.is_playing_desired = true;
                gstArray.nativePlay();
            }
        });

        ImageButton pause = (ImageButton) this.findViewById(R.id.button_stop);
        pause.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                gstArray.is_playing_desired = false;
                gstArray.nativePause();
            }
        });

        SurfaceView sv = (SurfaceView) this.findViewById(R.id.surface_video);
        SurfaceHolder sh = sv.getHolder();
        sh.addCallback(this);


        if (savedInstanceState != null) {
            gstArray.is_playing_desired = savedInstanceState.getBoolean("playing");
            Log.i ("GStreamer", "Activity created. Saved state is playing:" + gstArray.is_playing_desired);
        } else {
            gstArray.is_playing_desired = false;
            Log.i ("GStreamer", "Activity created. There is no saved state, playing: false");
        }



        Button exit = (Button) this.findViewById(R.id.btn_exit);
        exit.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
//                is_playing_desired = false;
//                nativePause();
//                nativeFinalize();
                finish();
            }
        });

//        gstSingle.state(savedInstanceState);
//        gstSingle.enableButtons();

        // Start with disabled buttons, until native code is initialized
        this.findViewById(R.id.button_play).setEnabled(false);
        this.findViewById(R.id.button_stop).setEnabled(false);

        gstArray.nativeInit();


    }

    protected void onSaveInstanceState (Bundle outState) {
        Log.d ("GStreamer", "Saving state, playing:" + gstArray.is_playing_desired);
        outState.putBoolean("playing", gstArray.is_playing_desired);
    }

    //Back button listener
    @Override
    public void onBackPressed() {
        //stopThread = true;
        gstArray.nativeFinalize();
        super.onBackPressed();
    }

    protected void onDestroy() {
        gstArray.nativeFinalize();
        super.onDestroy();
    }


    public void surfaceChanged(SurfaceHolder holder, int format, int width,
                               int height) {
        Log.d("GStreamer", "Surface changed to format " + format + " width "
                + width + " height " + height);
        gstArray.nativeSurfaceInit(holder.getSurface());
    }

    public void surfaceCreated(SurfaceHolder holder) {
        Log.d("GStreamer", "Surface created: " + holder.getSurface());
    }

    public void surfaceDestroyed(SurfaceHolder holder) {
        Log.d("GStreamer", "Surface destroyed");
        gstArray.nativeSurfaceFinalize();
    }



    // Called from native code. This sets the content of the TextView from the UI thread.
    private void setMessage(final String message) {
        final TextView tv = (TextView) this.findViewById(R.id.textview_message);
        runOnUiThread (new Runnable() {
            public void run() {
                tv.setText(message);
            }
        });
    }

    // Called from native code. Native code calls this once it has created its pipeline and
    // the main loop is running, so it is ready to accept commands.
    private void onGStreamerInitialized () {
        Log.i ("GStreamer", "Gst initialized. Restoring state, playing:" + gstArray.is_playing_desired);
        // Restore previous playing state
        if (gstArray.is_playing_desired) {
            gstArray.nativePlay();
        } else {
            gstArray.nativePause();
        }

        // Re-enable buttons, now that GStreamer is initialized
        final Activity activity = this;
        runOnUiThread(new Runnable() {
            public void run() {
                activity.findViewById(R.id.button_play).setEnabled(true);
                activity.findViewById(R.id.button_stop).setEnabled(true);
            }
        });
    }




//    static {
//        System.loadLibrary("gstreamer_android");
//        System.loadLibrary("tutorial-1");
//        nativeClassInit();
//    }



}
