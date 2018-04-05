import pytest
from eth_tester.exceptions import TransactionFailed
from tests.fixtures import (
    owner_index,
    owner,
    contract_params,
    create_contract,
    get_token_contract,
    get_accounts,
    create_accounts
)
from tests.fixtures_uraiden import token_contract


def test_token_mint(web3, token_contract, contract_params, get_accounts):
    decimals = contract_params['decimals']
    multiplier = 10**(decimals)
    supply = 10000 * multiplier
    (A, B) = get_accounts(2)
    token = token_contract()
    supply = token.call().totalSupply()
    token_pre_balance = web3.eth.getBalance(token.address)

    with pytest.raises(TypeError):
        token.transact({'from': A}).mint(-3)

    with pytest.raises(TransactionFailed):
        token.transact({'from': A}).mint()

    wei_value = 10**17 + 21000
    tokens = 50 * multiplier;
    token.transact({'from': A, 'value': wei_value}).mint()
    assert token.call().balanceOf(A) == tokens
    assert token.call().totalSupply() == supply + tokens
    assert web3.eth.getBalance(token.address) == token_pre_balance + wei_value
