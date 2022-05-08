using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BulletController : MonoBehaviour
{
    float speed= 0.5f;
	[SerializeField]
	float deadZone = 7f;



	private void FixedUpdate()
	{
		transform.position += new Vector3(0, speed/30, 0);

		if (transform.position.y > deadZone) Destroy(this.gameObject);
	}

	public void setSpeed(float nSpeed)
	{
		speed = nSpeed;
	}

	private void OnCollisionEnter2D(Collision2D collision)
	{
		Destroy(this.gameObject);
	}
}
