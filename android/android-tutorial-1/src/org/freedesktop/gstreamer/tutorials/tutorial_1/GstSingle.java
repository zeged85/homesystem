package org.freedesktop.gstreamer.tutorials.tutorial_1;
import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import org.freedesktop.gstreamer.GStreamer;

public class GstSingle implements SurfaceHolder.Callback{


    public native void nativeInit();     // Initialize native code, build pipeline, etc
    public native void nativeFinalize(); // Destroy pipeline and shutdown native code
    public native void nativePlay();     // Set pipeline to PLAYING
    public native void nativePause();    // Set pipeline to PAUSED
    public static native boolean nativeClassInit(); // Initialize native class: cache Method IDs for callbacks

    public native void nativeSurfaceInit(Object surface);
    public native void nativeSurfaceFinalize();

    public long native_custom_data;      // Native code will use this to keep private data

    public boolean is_playing_desired;   // Whether the user asked to go to PLAYING

    private Tutorial1 tutorial1;




    GstSingle(Tutorial1 main){
        System.out.println("in gstSingle!");

        tutorial1=main;

        try {
            GStreamer.init(main);
        } catch (Exception e) {
            Toast.makeText(main, e.getMessage(), Toast.LENGTH_LONG).show();
            main.finish();
            return;
        }




    }



    public void surfaceChanged(SurfaceHolder holder, int format, int width,
                               int height) {
        Log.d("GStreamer", "Surface changed to format " + format + " width "
                + width + " height " + height);
        nativeSurfaceInit(holder.getSurface());

//        gstArray2.nativeSurfaceInit(holder.getSurface());


    }

    public void surfaceCreated(SurfaceHolder holder) {
        Log.d("GStreamer", "Surface created: " + holder.getSurface());
    }

    public void surfaceDestroyed(SurfaceHolder holder) {
        Log.d("GStreamer", "Surface destroyed");
        nativeSurfaceFinalize();
//        gstArray2.nativeSurfaceFinalize();
    }




    public void state(Bundle savedInstanceState) {
        if (savedInstanceState != null) {
            is_playing_desired = savedInstanceState.getBoolean("playing");
            Log.i ("GStreamer", "Activity created. Saved state is playing:" + is_playing_desired);
        } else {
            is_playing_desired = false;
            Log.i ("GStreamer", "Activity created. There is no saved state, playing: false");
        }
    }

    public void enableButtons() {
        // Start with disabled buttons, until native code is initialized
        tutorial1.findViewById(R.id.button_play).setEnabled(false);
        tutorial1.findViewById(R.id.button_stop).setEnabled(false);

        nativeInit();
    }

    // Called from native code. This sets the content of the TextView from the UI thread.
    private void setMessage(final String message) {
        final TextView tv = (TextView) tutorial1.findViewById(R.id.textview_message);
        tutorial1.runOnUiThread (new Runnable() {
            public void run() {
                tv.setText(message);
            }
        });
    }

    // Called from native code. Native code calls this once it has created its pipeline and
    // the main loop is running, so it is ready to accept commands.
    private void onGStreamerInitialized () {
        Log.i ("GStreamer", "Gst initialized. Restoring state, playing:" + is_playing_desired);
        // Restore previous playing state
        if (is_playing_desired) {
            nativePlay();
        } else {
            nativePause();
        }

        // Re-enable buttons, now that GStreamer is initialized
        final Activity activity = tutorial1;
        tutorial1.runOnUiThread(new Runnable() {
            public void run() {
                activity.findViewById(R.id.button_play).setEnabled(true);
                activity.findViewById(R.id.button_stop).setEnabled(true);
                activity.findViewById(R.id.button_play2).setEnabled(true);
                activity.findViewById(R.id.button_stop2).setEnabled(true);
            }
        });
    }


    static {
        System.loadLibrary("gstreamer_android");
        System.loadLibrary("tutorial-1");
        nativeClassInit();
    }

}
