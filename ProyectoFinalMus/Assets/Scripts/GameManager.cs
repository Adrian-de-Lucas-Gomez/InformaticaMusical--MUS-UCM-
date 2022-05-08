using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using FMOD.Studio;
using FMODUnity;

public class GameManager : MonoBehaviour
{
	[SerializeField]
	int numEne1 = 3;
	[SerializeField]
	GameObject ene1;

	[SerializeField]
	int numEne2 = 2;
	[SerializeField]
	GameObject ene2;

	[SerializeField]
	int numEne3 = 1;
	[SerializeField]
	GameObject ene3;

	[SerializeField]
	int limits = 9;
	[SerializeField]
	float posEne1 = 5;
	[SerializeField]
	float separacion = 2;
	[SerializeField]
	StudioEventEmitter eventEmitter;

    List<int> enemiesCount = new List<int>();

    private static GameManager instance;
    public static GameManager Instance
    {
        get
        {
            return instance;
        }
    }

	private void Awake()
	{
        if (instance == null)
        {
            instance = this;
        }
    }

	// Start is called before the first frame update
	void Start()
    {
        eventEmitter.SetParameter("EnemyType-1", 1);
        eventEmitter.SetParameter("EnemyType-2", 1);
        eventEmitter.SetParameter("EnemyType-3", 1);

        enemiesCount.Add(numEne1);
        enemiesCount.Add(numEne2);
        enemiesCount.Add(numEne3);

        float spawny = posEne1;
        float spawnx;

        float distx = ((2 * limits) / (numEne1 + 1));
        float startx = (distx - limits);
        for (int i = 0; i < numEne1; i++)
		{
            spawnx = startx + distx * i;
            Instantiate(ene1, new Vector3(spawnx,spawny), Quaternion.identity);
		}
        spawny -= separacion; spawnx = 0;

         distx = ((2 * limits) / (numEne2 + 1));
        startx = (distx - limits);
        for (int i = 0; i < numEne2; i++)
        {
            spawnx = startx + distx * i;
            Instantiate(ene2, new Vector3(spawnx, spawny), Quaternion.identity);
        }
        spawny -= separacion; spawnx = 0;

        distx = ((2 * limits) / (numEne3 + 1));
        startx = (distx - limits);
        for (int i = 0; i < numEne3; i++)
        {
            spawnx = startx + distx * i;
            Instantiate(ene3, new Vector3(spawnx, spawny), Quaternion.identity);
        }
    }

    // Update is called once per frame
    void Update()
    {

    }

    public void PlayerHealthUpdate(int playerHealth)
	{
        eventEmitter.SetParameter("Health", (float)playerHealth);
    }

    public void EnemyDead(int index)
	{
        enemiesCount[index]--;
        if(enemiesCount[index]<= 0)
		{
            string paramName = "";
			switch (index)
			{
				case 0:
                    paramName = "EnemyType-1";
                    break;
                case 1:
                    paramName = "EnemyType-2";
                    break;
                case 2:
                    paramName = "EnemyType-3";
                    break;
            }

            eventEmitter.SetParameter(paramName, 0);            
		}

        float enemPer100 = (enemiesCount[0] + enemiesCount[1] + enemiesCount[2])/(numEne1+numEne2+numEne3) * 100;

        eventEmitter.SetParameter("PorcentajeEnemigos", enemPer100);
    }
}
