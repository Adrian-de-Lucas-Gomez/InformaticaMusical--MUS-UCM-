using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class PlayerController : MonoBehaviour
{
	[SerializeField]
	float speed = 1.0f;
	[SerializeField]
	float limit = 4.0f;
	[SerializeField]
	GameObject shootingPivot;
	[SerializeField]
	GameObject proyectile;
	[SerializeField]
	float proyectileSpeed = 0.5f;
	[SerializeField]
	int maxLife = 100;
	[SerializeField]
	int dmgTick = 20;
	[SerializeField]
	TextMeshProUGUI lifeText;



	float inputSpeed;
	int life;

	private void Start()
	{
		life = maxLife;
	}

	// Update is called once per frame
	void Update()
	{
		inputSpeed = 0;
		if (Input.GetKey(KeyCode.A)) inputSpeed -= 1;
		if (Input.GetKey(KeyCode.D)) inputSpeed += 1;

		if (Input.GetKeyDown(KeyCode.Space))
		{
			GameObject b = Instantiate(proyectile, shootingPivot.transform.position, Quaternion.Euler(0, 0, 45));
			b.GetComponent<BulletController>().setSpeed(proyectileSpeed);
		}
	}

	private void FixedUpdate()
	{
		gameObject.transform.position += new Vector3(inputSpeed * speed/30, 0, 0);

		float absPosX = Mathf.Abs(gameObject.transform.position.x);
		if (absPosX > limit) gameObject.transform.position -= new Vector3(inputSpeed * speed/30, 0, 0);

	}

	private void OnCollisionEnter2D(Collision2D collision)
	{
		life -= dmgTick;
		if (life <= 0) Destroy(this.gameObject);
		lifeText.text = "Health: "+life;
	}
}
