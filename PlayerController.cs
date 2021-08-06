using System.Collections;
using System.Collections.Generic;
//using System.Numerics;
using UnityEngine;
using UnityStandardAssets.CrossPlatformInput;

public class PlayerController : MonoBehaviour
{
    //Config
    [SerializeField] float moveSpeed = 4f;
    [SerializeField] float jumpForce = 4f;
    [SerializeField] float climbSpeed = 3f;
    [SerializeField] Vector2 deathKick = new Vector2(10f, 10f);
    public Vector3 respawnPoint;

    //State
    bool isAlive = true;

    // cached Components
    Rigidbody2D playerRigidBody;
    [HideInInspector] public Animator playerAnimator;
    CapsuleCollider2D playerCollider;   //hit collider
    BoxCollider2D playerFeetCollider; //for checking if can jump from ground
    float gravityScaleAtStart;  //concerning climbing..


    // Start is called before the first frame update
    void Start()
    {
        playerRigidBody = GetComponent<Rigidbody2D>();
        playerAnimator = GetComponent<Animator>();
        playerCollider = GetComponent<CapsuleCollider2D>();
        playerFeetCollider = GetComponent<BoxCollider2D>();
        gravityScaleAtStart = playerRigidBody.gravityScale;
        respawnPoint = transform.position;
    }

    // Update is called once per frame
    void Update()
    {
        if (!isAlive) { return; }

        Move();
        Jump();
        Fall();
        Climb();
        FlipSprite();
        Die();

    }

    private void Move()
    {
        if ((playerFeetCollider.IsTouchingLayers(LayerMask.GetMask("Ground")) ||
            playerFeetCollider.IsTouchingLayers(LayerMask.GetMask("Ladder")) ||
            playerFeetCollider.IsTouchingLayers(LayerMask.GetMask("Block"))
            && playerRigidBody.velocity.y == 0))
        {
            playerAnimator.SetBool("jumping", false);
            playerAnimator.SetBool("falling", false);
            playerAnimator.SetBool("moving", true);
        }


        //this bool in FlipSprite() also..
        bool playerHasHorizontalSpeed = Mathf.Abs(playerRigidBody.velocity.x) > Mathf.Epsilon;
        {
            playerAnimator.SetBool("moving", playerHasHorizontalSpeed);
        }

    }

    private void Jump()
    {
        //if player is not touching ground, can't jump
        if (!playerFeetCollider.IsTouchingLayers(LayerMask.GetMask("Ground"))
            && !playerFeetCollider.IsTouchingLayers(LayerMask.GetMask("Block"))
            )
        {
            playerAnimator.SetBool("jumping", true);
            return;
        }
        //do jump action (if touching ground)
        if (CrossPlatformInputManager.GetButtonDown("Jump"))
        {
            Vector2 jumpVelocity = new Vector2(0f, jumpForce);
            playerRigidBody.velocity += jumpVelocity;
            playerAnimator.SetBool("jumping", true);
        }
    }

    private void Fall()
    {
        //if player moving downwards & not touching ground or block or anything
        if (playerRigidBody.velocity.y < 0f
            && !playerFeetCollider.IsTouchingLayers(LayerMask.GetMask("Ground"))
            && !playerFeetCollider.IsTouchingLayers(LayerMask.GetMask("Block")))
        {
            playerAnimator.SetBool("falling", true);
        }
        else
        {
            playerAnimator.SetBool("falling", false);
        }
    }

    private void Climb()
    {   //Feetcollider check here, so doesn't get stuck when walking from ladders
        if (!playerFeetCollider.IsTouchingLayers(LayerMask.GetMask("Ladder")))
        {
            playerRigidBody.gravityScale = gravityScaleAtStart;
            return;
        }

        float controlThrow = CrossPlatformInputManager.GetAxis("Vertical");
        Vector2 climbVelocity = new Vector2(playerRigidBody.velocity.x, controlThrow * climbSpeed);
        playerRigidBody.velocity = climbVelocity;
        playerRigidBody.gravityScale = 0;
    }

    private void Die()
    {

        if (playerCollider.IsTouchingLayers(LayerMask.GetMask("Enemy")))
        {
            playerAnimator.SetTrigger("dying");
            playerFeetCollider.enabled = false;     //deactivate boxcollider doesn't stay standing
            playerRigidBody.freezeRotation = false; //body can roll over
            GetComponent<Rigidbody2D>().AddTorque(1, ForceMode2D.Impulse);  //force for "animation"
            playerCollider.sharedMaterial = null;   //remove friction so body isn't too slippery 
            isAlive = false;
            FindObjectOfType<GameSession>().ProcessPlayerDeath();
        }
    }

    private void FlipSprite()
    {
        //bool absolute horizontal speed is greater than zero (?)
        bool playerHasHorizontalSpeed = Mathf.Abs(playerRigidBody.velocity.x) > Mathf.Epsilon;
        if (playerHasHorizontalSpeed)
        {
            //if has speed, Vector2 becomes +1 or -1, depending on the sign ofmovement
            //y stays 1f
            transform.localScale = new Vector2(Mathf.Sign(playerRigidBody.velocity.x), 1f);
        }
    }
}
