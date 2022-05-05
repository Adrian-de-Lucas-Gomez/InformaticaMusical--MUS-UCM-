using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
	[SerializeField]
	float speed = 1.0f;
	[SerializeField]
	float limit = 8.0f;
	[SerializeField]
	GameObject shootingPivot;
	[SerializeField]
	GameObject proyectile;
	[SerializeField]
	float proyectileSpeed = 0.5f;



	float inputSpeed;

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
		gameObject.transform.position += new Vector3(inputSpeed * speed, 0, 0);

		float absPosX = Mathf.Abs(gameObject.transform.position.x);
		if (absPosX > limit) gameObject.transform.position -= new Vector3(inputSpeed * speed, 0, 0);

	}
}
