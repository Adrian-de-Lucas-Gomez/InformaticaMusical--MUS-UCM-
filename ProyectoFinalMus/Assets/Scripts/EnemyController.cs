using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyController : MonoBehaviour
{
    [SerializeField]
    GameObject shootingPivot;
    [SerializeField]
    GameObject proyectile;
    [SerializeField]
    float proyectileSpeed = 0.5f;
    [SerializeField]
    float timeToFirst = 3f;
    [SerializeField]
    float timeBetweenShots = 2f;
    [SerializeField]
    float limit = 4.0f;
    [SerializeField]
    float movementSpeed = 0.6f;
    [SerializeField]
    int enemyIndex = -1;

    int direction = 1;

    // Start is called before the first frame update
    void Start()
    {
        InvokeRepeating("Shoot", timeToFirst, timeBetweenShots);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

	private void FixedUpdate()
	{
        gameObject.transform.position += new Vector3(movementSpeed * direction / 30, 0, 0);

        float absPosX = Mathf.Abs(gameObject.transform.position.x);
        if (absPosX > limit) direction *= -1;
    }

	private void OnCollisionEnter2D(Collision2D collision)
	{
        GameManager.Instance.EnemyDead(enemyIndex);
        Destroy(this.gameObject);
	}

    private void Shoot()
	{
        GameObject b = Instantiate(proyectile, shootingPivot.transform.position, Quaternion.identity);
        b.GetComponent<enemyBullet>().setSpeed(proyectileSpeed);
    }
}
