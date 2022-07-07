using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Main : MonoBehaviour
{
    private string state = "Intro";
    private List<string> states = new List<string>(){
        "Intro",
        "Spin",
        // "Win",
        // "Lose",
        // "Noise",
    };

    private GameObject spinner;

    // Start is called before the first frame update
    void Start()
    {
        spinner = GameObject.Find("Spinner");
        changeState("Intro");

    }

    // Update is called once per frame
    void Update()
    {

    }
    
    private void makeVisible(GameObject obj) {
        // set scale to 0 



        obj.transform.localScale = new Vector3(1, 1, 1);

        // foreach (var child in obj.GetComponentsInChildren<Canvas>()) {
        //     child.enabled = true;
        // }
    }

    private void makeInvisible(GameObject obj) {
        obj.transform.localScale = new Vector3(0, 0, 0);

        // foreach (var child in obj.GetComponentsInChildren<Canvas>()) {
        //     child.enabled = false;
        // }
    }


    private void changeState(string newState){
        state = newState;
        // set the new state to visible
        var stateGameObject = GameObject.Find(state);
        makeVisible(stateGameObject);
        

        // set all other states to false
        for(int i = 0; i < states.Count; i++){
            if(states[i] != state){
                print("setting " + states[i] + " to invisible");
                stateGameObject = GameObject.Find(states[i]);
                makeInvisible(stateGameObject);
            }
        }
    }

    public void StartGame()
    {
        state = "Spin";
        changeState(state);
    }

    public void Intro()
    {
        state = "Intro";
        changeState(state);
    }
}
