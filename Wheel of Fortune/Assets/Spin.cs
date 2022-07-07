using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Spin : MonoBehaviour
{
    public bool isSpinning = false;
    public int duration = 3;

    // Start is called before the first frame update
    void Start()
    {

    }

    public void StartSpinning()
    {
        isSpinning = true;
        // start coroutine
        StartCoroutine(SpinCoroutine());
    }



    IEnumerator SpinCoroutine()
    {
        // wait for 3 seconds
        yield return new WaitForSeconds(3);
        isSpinning = false;
        
    }

    // Update is called once per frame
    void Update()
    {
        if (isSpinning) {
            transform.Rotate(0, 0, -3);
        }
    }
}
